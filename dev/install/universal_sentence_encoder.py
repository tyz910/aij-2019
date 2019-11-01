import tensorflow as tf
import tensorflow_hub as hub
import tf_sentencepiece

g = tf.Graph()
with g.as_default():
    text_input = tf.placeholder(dtype=tf.string, shape=[None])
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-multilingual/1")
    embedded_text = embed(text_input)
    init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
g.finalize()

session = tf.Session(graph=g)
session.run(init_op)

print(session.run(embedded_text, feed_dict={text_input: [
    "I enjoy taking long walks along the beach with my dog.",
]}))
