from ufal.udpipe import Model, Pipeline
from lib.sberbank.utils import sber_path, sber_encode, sber_decode
from lib.util.speller import Speller

from typing import Optional


class SyntaxNode:
    def __init__(self, tree, data, speller):
        self.tree = tree

        self.id = int(data[0]) - 1
        self.word = data[1]
        self.normal_form = data[2]
        self.POS = data[3]
        self.morph = data[5]
        self.morph2 = speller.parse_morph(self.word)
        self.link = None
        if data[6] != '0':
            self.link = int(data[6]) - 1

        self.link_type = data[7]

    def get_link(self, ignore_types=None):
        node = self

        while True:
            if node.link is None:
                return None

            node = self.tree.nodes[node.link]

            if ignore_types is not None and node.link_type in ignore_types:
                continue

            return node

    def __repr__(self):
        return f'#{self.id}, {self.link_type} -> #{self.link}, "{self.word}" [{self.normal_form}, {self.POS}, {self.morph}]'


class SyntaxTree:
    def __init__(self, syntax, speller):
        self.nodes = []

        for token in syntax:
            node = SyntaxNode(self, token, speller)
            self.nodes.append(node)

    def __repr__(self):
        return '\n'.join([str(node) for node in self.nodes])


class SyntaxParser:
    def __init__(self, speller: Optional[Speller] = None):
        self.udpipe_model = Model.load(sber_encode(sber_path('/var/sberbank/udpipe_syntagrus.model')))
        self.process_pipeline = Pipeline(self.udpipe_model, sber_encode('tokenize'), Pipeline.DEFAULT, Pipeline.DEFAULT,
                                         sber_encode('conllu'))

        if speller is None:
            speller = Speller()
        self.speller: Speller = speller

    def get_syntax(self, text):
        processed = self.process_pipeline.process(sber_encode(text))
        content = [l for l in sber_decode(processed).split('\n') if not l.startswith('#')]
        tagged = [w.split('\t') for w in content if w]
        return SyntaxTree(tagged, self.speller)
