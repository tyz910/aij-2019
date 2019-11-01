import os
import warnings
import pickle

from typing import List, Dict, Optional
Vocab = Dict[str, List[int]]

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from russtress import Accent


class Stress:
    def __init__(self, vocab: Optional[Vocab] = None, accent: Optional[Accent] = None):
        if vocab is None:
            vocab_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/stress')
            with open(vocab_dir + '/vocab.pickle', 'rb') as f:
                vocab = pickle.load(f)
        self.vocab: Vocab = vocab

        if accent is None:
            accent = Accent()
        self.accent: Accent = accent

    def from_vocab(self, word: str) -> Optional[List[int]]:
        word = word.lower()
        if word in self.vocab:
            return self.vocab[word]
        else:
            return None

    def from_model(self, word: str) -> List[int]:
        word = word.lower()
        stressed_word = self.accent.put_stress(word, stress_symbol="|!|")
        return [stressed_word.rfind("|!|") - 1]
