# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: encoder.py
# time: 2:31 下午

import numpy as np
import tensorflow as tf
from kashgari.embeddings.abc_embedding import ABCEmbedding


class GRUEncoder(tf.keras.Model):
    def __init__(self, embedding: ABCEmbedding, hidden_size: int = 1024):
        super(GRUEncoder, self).__init__()
        self.embedding = embedding
        self.gru = tf.keras.layers.GRU(hidden_size,
                                       return_sequences=True,
                                       return_state=True,
                                       recurrent_initializer='glorot_uniform')

    def call(self, x: np.ndarray, hidden: np.ndarray) -> np.ndarray:
        x = self.embedding.embed_model(x)
        output, state = self.gru(x, initial_state=hidden)
        return output, state


if __name__ == "__main__":
    pass