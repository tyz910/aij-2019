import os
import re
import glob
import unicodedata
import faiss
import numpy as np
from lib.util.sentence_encoder import SentenceEncoder
from typing import List, Dict, Optional


class Esse:
    def __init__(self, data: Dict[str, str]):
        self.id: str = ''
        self.title: str = ''
        self.text: str = ''
        self.problem: str = ''
        self.conclusion: str = ''
        self.position1: str = ''
        self.position2: str = ''
        self.reference: str = ''
        self.examples: List[str] = []

        if 'id' in data:
            self.id = data['id']

        if 'title' in data:
            self.title = data['title']

        if 'text' in data:
            self.text = data['text']

        if 'problem' in data:
            self.problem = data['problem']

        if 'conclusion' in data:
            self.conclusion = data['conclusion']

        if 'position1' in data:
            self.position1 = data['position1']

        if 'position2' in data:
            self.position2 = data['position2']

        if 'reference' in data:
            self.reference = data['reference']

        if 'example1' in data:
            self.examples.append(data['example1'])

        if 'example2' in data:
            self.examples.append(data['example2'])

        if 'example3' in data:
            self.examples.append(data['example3'])

    def get_index_text(self) -> str:
        if self.text != '':
            return ''
            return self.text
        else:
            # if self.problem == '' or (self.position1 == '' and self.position2 == '' and self.conclusion == ''):
            #     return ''

            text = ' '.join([
                self.problem,
                self.conclusion,
                self.position1,
                self.position2,
                self.reference,
            ])

            text = text.replace('\n', ' ')
            text = re.sub(r'[\s]+', ' ', text).strip()

            return text

    def __repr__(self) -> str:
        return {
            'id': self.id,
            'title': self.title,
            'problem': self.problem,
            'position1': self.position1,
            'position2': self.position2,
            'conclusion': self.conclusion,
            'examples': self.examples,
        }.__repr__()


class EsseLoader:
    def __init__(self, sentence_encoder: Optional[SentenceEncoder] = None):
        self.esses: List[Esse] = []
        self.__load_esses()

        if sentence_encoder is None:
            sentence_encoder = SentenceEncoder()
        self.sentence_encoder: SentenceEncoder = sentence_encoder

        self.index: faiss.IndexFlatIP = faiss.IndexFlatIP(512)
        self.__load_index()

    def make_esse(self, text: str) -> Esse:
        esse = Esse({})
        positions = []
        examples = []

        for e in self.search(text):
            if e.problem != '' and esse.problem == '':
                esse.problem = e.problem

            if e.conclusion != '' and esse.conclusion == '':
                esse.conclusion = e.conclusion

            if e.position1 != '':
                positions.append(e.position1)

            if e.position2 != '':
                positions.append(e.position2)

            examples += e.examples

        if len(positions) > 1:
            esse.position1 = positions[0]

        if len(positions) > 2:
            esse.position2 = positions[1]

        esse.examples = examples[:2]

        return esse

    def search(self, text: str, top_n: int = 3) -> List[Esse]:
        text_emb = self.sentence_encoder.encode([text])
        score, idx = self.index.search(text_emb, top_n)
        return [self.esses[i] for i in idx[0]]

    def update_index(self):
        path = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/esse/embeddings.npy')
        embeddings = self.sentence_encoder.encode([esse.get_index_text() for esse in self.esses])
        np.save(path, embeddings)

        self.index = faiss.IndexFlatIP(512)
        self.index.add(embeddings)

    def __load_esses(self):
        path = os.path.abspath(os.path.dirname(__file__) + '/../../var/data/esse')
        for filepath in sorted(glob.glob(f"{path}/*.txt")):
            with open(filepath) as f:
                esse_tpl = {}
                block = None

                for part in re.split(r'\[([a-z0-9]{4,})\]', f.read()):
                    part = unicodedata.normalize("NFKD", part).strip()
                    if part != '':
                        if part in ['title', 'text', 'problem', 'conclusion', 'position1', 'position2', 'example1', 'example2', 'example3', 'reference', 'ignore']:
                            block = part
                        else:
                            esse_tpl[block] = part

                if 'ignore' in esse_tpl:
                    continue

                esse_tpl['id'] = filepath.split('/')[-1]

                esse = Esse(esse_tpl)
                if esse.get_index_text() != '':
                    self.esses.append(esse)

    def __load_index(self):
        path = os.path.abspath(os.path.dirname(__file__) + '/../../var/model/esse/embeddings.npy')
        if os.path.isfile(path):
            embeddings = np.load(path)
            self.index.add(embeddings)
        else:
            self.update_index()
