
import numpy as np
import gensim
from scipy import spatial

model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True, limit=500000)
print("Loaded model")
index2word_set = set(model.wv.index2word)

def avg_feature_vector(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

def make_sentence(name):

    words = []
    if('_' in name): #if snake case
        name = name.lower()
        words = name.split('_')
    else: #identify if camel case
        word = ""
        for c in name:
            if(c.islower()):
                word +=c
            else:
                words.append(word)
                word = ""
                word += c.lower()
        words.append(word)

    sentence = ""
    for w in words:
        sentence += w
        sentence += " "
    return sentence[:-1]

s1_afv = avg_feature_vector(make_sentence("getFirst"), model=model, num_features=300, index2word_set=index2word_set)
s2_afv = avg_feature_vector(make_sentence("getTop"), model=model, num_features=300, index2word_set=index2word_set)
sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
print(sim)
