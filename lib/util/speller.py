import os
import pymorphy2
from deeppavlov import build_model, configs

from typing import Set, Dict


class Speller:
    def __init__(self):
        self.model = None
        self.morph = None
        self.dict_words: Set[str] = set()
        self.vocab: Set[str] = set()
        self.examples: Dict[str, Set[str]] = {}

        self.__load_vocab()

    def __load_vocab(self):
        model_dir = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/spell')
        with open(model_dir + '/vocab.txt', 'r') as f:
            for line in f:
                parts = line.split(' ')
                word = parts[0].lower().replace('ё', 'е').strip()
                char = ''
                if len(parts) > 1:
                    char = parts[1].lower().replace('ё', 'е').strip()

                self.vocab.add(word.replace('..', char))
                if word not in self.examples:
                    self.examples[word] = set()
                self.examples[word].add(char)

        with open(model_dir + '/dict_words.txt', 'r') as f:
            for line in f:
                self.dict_words.add(line.lower().strip())

    def correct(self, word: str) -> str:
        if self.model is None:
            self.model = build_model(configs.spelling_correction.levenshtein_corrector_ru, download=False)

        return self.model([word])[0]

    def is_correct(self, word: str) -> bool:
        return self.correct(word) == word

    def is_known(self, word: str) -> bool:
        if self.morph is None:
            self.morph = pymorphy2.MorphAnalyzer()

        return self.morph.word_is_known(word)

    def in_vocab(self, word: str) -> bool:
        return word in self.vocab

    def in_dict_words(self, word: str) -> bool:
        return word in self.dict_words

    def parse_morph(self, word: str) -> pymorphy2.analyzer.Parse:
        if self.morph is None:
            self.morph = pymorphy2.MorphAnalyzer()

        return self.morph.parse(word)[0]

    def try_inflect(self, word: str, tag: str) -> str:
        try:
            return self.parse_morph(word).inflect({tag}).word
        except:
            return word

    def inflect_like(self, original_word: str, inflect_word: str) -> str:
        tag = self.parse_morph(original_word).tag

        inflect_word = self.try_inflect(inflect_word, tag.gender)
        inflect_word = self.try_inflect(inflect_word, tag.number)
        inflect_word = self.try_inflect(inflect_word, tag.case)

        return inflect_word
