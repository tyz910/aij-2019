import os
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pytorch_transformers import BertConfig, BertModel, BertForMaskedLM, BertTokenizer
from typing import List, Tuple, Optional


class BertOutput:
    def __init__(self, token_ids: np.array, clf: np.array, token_embeddings: np.array):
        self.token_ids: np.array = token_ids
        self.clf: np.array = clf
        self.token_embeddings: np.array = token_embeddings
        self.sentence_embeddings: Optional[np.array] = None

    def get_clf_output(self) -> np.array:
        return self.clf

    def get_token_embeddings(self, token_positions: List[int], num_layers: int = 4, pool_mean: bool = False) -> np.array:
        emb = np.hstack(self.token_embeddings[-num_layers:, token_positions, :])
        if pool_mean:
            emb = np.mean(emb, axis=0)

        return emb

    def get_sentence_embeddings(self) -> np.array:
        if self.sentence_embeddings is None:
            self.sentence_embeddings = np.mean(self.token_embeddings, axis=1)

        return self.sentence_embeddings

    def get_similarity(self, other: 'BertOutput') -> np.array:
        self_embeddings = self.get_sentence_embeddings()
        other_embeddings = other.get_sentence_embeddings()

        return np.array([
            cosine_similarity([self_embeddings[i]], [other_embeddings[i]])[0, 0] for i, _ in enumerate(self_embeddings)
        ])


class Bert:
    def __init__(self):
        model_dir = '/var/model/bert'
        if not os.path.isdir(model_dir):
            model_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/bert')

        self.use_gpu: bool = torch.cuda.is_available()
        self.config: BertConfig = BertConfig.from_json_file(model_dir + '/config.json')
        self.tokenizer: BertTokenizer = BertTokenizer.from_pretrained(model_dir + '/vocab.txt', do_lower_case=False)

        self.model_masked: BertForMaskedLM = BertForMaskedLM.from_pretrained(model_dir + '/model.bin', config=self.config)
        self.model: BertModel = self.model_masked.bert

        # freeze bert encoder
        for param in self.model.parameters():
            param.requires_grad = False
        for param in self.model_masked.parameters():
            param.requires_grad = False

        self.model.encoder.output_hidden_states = True
        self.model.eval()
        self.model_masked.eval()

        if self.use_gpu:
            self.model.cuda()
            self.model_masked.cuda()

    def eval(self, sentence_a: str, sentence_b: Optional[str] = None) -> BertOutput:
        token_ids, token_type_ids = self.tokenize(sentence_a, sentence_b)
        if self.use_gpu:
            token_ids, token_type_ids = token_ids.cuda(), token_type_ids.cuda()

        _, clf, encoded_layers = self.model(token_ids, token_type_ids)
        token_embeddings = []
        for layer in encoded_layers:
            token_embeddings.append(layer.cpu().numpy()[0])

        return BertOutput(
            token_ids.cpu().numpy()[0],
            clf.cpu().numpy()[0],
            np.array(token_embeddings)
        )

    def tokenize(self, sentence_a: str, sentence_b: Optional[str] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        t = self.tokenizer

        tokens_a = [t.cls_token] + t.tokenize(sentence_a) + [t.sep_token]
        token_type_ids = [0] * len(tokens_a)

        if sentence_b is not None:
            tokens_b = t.tokenize(sentence_b) + [t.sep_token]
            token_type_ids += [1] * len(tokens_b)
        else:
            tokens_b = []

        token_ids = t.convert_tokens_to_ids(tokens_a + tokens_b)
        return torch.tensor([token_ids[:512]]), torch.tensor([token_type_ids[:512]])

    def get_token_positions(self, sentence: str, word: str) -> List[int]:
        start_idx = len(self.tokenizer.tokenize(sentence.split(word)[0]))
        end_idx = start_idx + len(self.tokenizer.tokenize(word))

        return list(range(start_idx, end_idx))

    def predict_masked_token(self, text: str, num_words: int = 10) -> List[str]:
        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segments_ids = [0] * len(tokens)

        tokens_tensor = torch.tensor([token_ids[:512]])
        segments_tensors = torch.tensor([segments_ids[:512]])

        if self.use_gpu:
            tokens_tensor, segments_tensors = tokens_tensor.cuda(), segments_tensors.cuda()

        predictions = self.model_masked(tokens_tensor, segments_tensors)

        masked_index = tokens.index('[MASK]')
        tokens_idx = torch.argsort(predictions[0][0][masked_index])[-num_words:].cpu().numpy()

        return self.tokenizer.convert_ids_to_tokens(np.flip(tokens_idx))

    def get_word_in_text_scores(self, text: str, word: str) -> np.array:
        word_tokens = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(word))
        text = '[CLS] ' + text + ' [SEP]'
        text = text.replace('[MASK]', '[MASK]' * len(word_tokens))

        tokens = self.tokenizer.tokenize(text)
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        segments_ids = [0] * len(tokens)

        tokens_tensor = torch.tensor([token_ids[:512]])
        segments_tensors = torch.tensor([segments_ids[:512]])

        if self.use_gpu:
            tokens_tensor, segments_tensors = tokens_tensor.cuda(), segments_tensors.cuda()

        predictions = self.model_masked(tokens_tensor, segments_tensors)

        mask_idx = tokens.index('[MASK]')
        scores = []
        for token in word_tokens:
            scores.append(torch.nn.functional.softmax(predictions[0][0][mask_idx])[token].item())
            mask_idx += 1

        return np.array(scores)

    def get_replace_proba(self, text: str, original_word: str, replace_word: str) -> float:
        text = text.replace(original_word, '[MASK]')
        proba_original = self.get_word_in_text_scores(text, original_word)
        proba_replace = self.get_word_in_text_scores(text, replace_word)

        for proba1, proba2 in zip(proba_original, proba_replace):
            if proba1 != proba2:
                return proba2 / proba1

        return 0.0
