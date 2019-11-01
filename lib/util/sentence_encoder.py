import numpy as np
import warnings
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional, Sequence

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    import tensorflow as tf
    import tensorflow_hub as hub
    import tf_sentencepiece


class SentenceEncoder:
    def __init__(self):
        self.session: Optional[tf.Session] = None
        self.embedded_text: Optional[tf.Tensor] = None
        self.text_input: Optional[tf.Tensor] = None

    def encode(self, sentences: Sequence[str]) -> np.array:
        if self.session is None:
            self.__session_init()

        return self.session.run(self.embedded_text, feed_dict={self.text_input: sentences})

    def get_similarity(self, sentence_a: str, sentence_b: str) -> np.array:
        emb = self.encode([sentence_a, sentence_b])
        return cosine_similarity([emb[0]], [emb[1]])[0]

    def __session_init(self):
        g = tf.Graph()
        with g.as_default():
            text_input = tf.placeholder(dtype=tf.string, shape=[None])
            embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-multilingual/1")
            embedded_text = embed(text_input)
            init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
        g.finalize()

        session = tf.Session(graph=g)
        session.run(init_op)

        self.session = session
        self.embedded_text = embedded_text
        self.text_input = text_input
