#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import keras
from keras import ops
from keras import layers

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super().__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output)
        return self.layernorm2(out1 + ffn_output)

class PositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        self.maxlen = maxlen
        super().__init__()
        #self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        #self.token_emb = layers.Dense(embed_dim, input_dim=vocab_size)
        self.token_emb = keras.layers.CategoryEncoding(num_tokens=vocab_size,output_mode="one_hot")
        
    def call(self, x):
        #positions = ops.arange(start=0, stop=self.maxlen, step=1)
        #positions = self.pos_emb(positions)
        #x = self.token_emb(x)
        return x #+ positions

class PositionEmbeddingFixedWeights(layers.Layer):
    def __init__(self, sequence_length, vocab_size, output_dim, **kwargs):
        super(PositionEmbeddingFixedWeights, self).__init__(**kwargs)
        word_embedding_matrix = self.get_position_encoding(vocab_size, output_dim)   
        position_embedding_matrix = self.get_position_encoding(sequence_length, output_dim)                                          
        self.word_embedding_layer = layers.Embedding(
            input_dim=vocab_size, output_dim=output_dim,
            weights=[word_embedding_matrix],
            trainable=False
        )
        self.position_embedding_layer = layers.Embedding(
            input_dim=sequence_length, output_dim=output_dim,
            weights=[position_embedding_matrix],
            trainable=False
        )
             
    def get_position_encoding(self, seq_len, d, n=10000):
        P = np.zeros((seq_len, d))
        for k in range(seq_len):
            for i in np.arange(int(d/2)):
                denominator = np.power(n, 2*i/d)
                P[k, 2*i] = np.sin(k/denominator)
                P[k, 2*i+1] = np.cos(k/denominator)
        return P
  
    def call(self, inputs):        
        position_indices = ops.range(ops.shape(inputs)[-1])
        embedded_words = self.word_embedding_layer(inputs)
        embedded_indices = self.position_embedding_layer(position_indices)
        return embedded_words + embedded_indices

print("load small.most_similar…")
from small import most_similar, d_corpus

print(len(d_corpus.keys()), "words")
words = list(d_corpus.keys())[:10_000]

#from tokenizer import Tokenizer
#def tokenize(word):
#    return list(word.encode("utf-8"))

print("create training data…")
maxlen = max([len(w) for w in words])
vocab = dict([[c,i] for [i,c] in enumerate(set("".join(words)))])
vocab_size = len(vocab)

one_hot = keras.layers.CategoryEncoding(num_tokens=vocab_size,output_mode="one_hot")
def tokenize(word):
    #return [vocab[c] for c in word]
    return [one_hot(vocab[c]) for c in word]

print("create tokens…")
tokens = keras.utils.pad_sequences([tokenize(word)[:maxlen] for word in words], maxlen=maxlen)
print("create embeddings…")
embeddings = list(d_corpus.values())[:len(tokens)]

#import joblib
#joblib.dump({"tokens":tokens, "embeddings":embeddings}, "dataset")
#data = joblib.load("/home/j03/Documents/src/py/lm/tokenize/src/dataset_small"); tokens = data["tokens"]; embeddings = data["embeddings"]

print("split…")
train_size = int(.9*len(words))
x_train = np.array(tokens[:train_size])
y_train = np.array(embeddings[:train_size])
x_val = np.array(tokens[train_size:])
y_val = np.array(embeddings[train_size:])
print(len(x_train), "Training sequences")
print(len(x_val), "Validation sequences")


embed_dim = vocab_size  # Embedding size for each token
num_heads = 2  # Number of attention heads
ff_dim = len(words)  # Hidden layer size in feed forward network inside transformer

#embedding_layer = PositionEmbeddingFixedWeights(maxlen, vocab_size, embed_dim)
embedding_layer = PositionEmbedding(maxlen, vocab_size, embed_dim)
transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)

inputs = layers.Input(shape=(maxlen,vocab_size))
x = inputs
#x = keras.layers.CategoryEncoding(num_tokens=vocab_size,output_mode="one_hot")(x)
x = embedding_layer(inputs)
x = transformer_block(x)
x = layers.GlobalAveragePooling1D()(x)
x = layers.Dropout(0.1)(x)
x = layers.Dense(20, activation="relu")(x)
x = layers.Dropout(0.1)(x)
outputs = layers.Dense(100)(x)

model = keras.Model(inputs=inputs, outputs=outputs)

print("compile…")
model.compile(optimizer="adam", loss="mean_squared_error")
model.summary()

print("fit…")
callbacks = [keras.callbacks.ModelCheckpoint(filepath="../example/model.weights.h5",
                                             save_weights_only=True,
                                             save_best_only=True,
                                             verbose=1)]

history = model.fit(
    x_train, y_train, epochs=1000, validation_data=(x_val, y_val), callbacks=callbacks
)
model.save("../example/model.keras", overwrite=True)

#y_pred = model.predict(x_train)
for word in words[:train_size][:20]:
    pred = model.predict(keras.utils.pad_sequences([tokenize(word)[:maxlen]], maxlen=maxlen))[0]
    print(word, ":\n", most_similar(pred,3),"\n")