
import numpy as np
import gensim
import requests
import json
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

def make_list(name):
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
    return words

def make_sentence(words):
    sentence = ""
    for w in words:
        sentence += w
        sentence += " "
    return sentence[:-1]

def similarity_sentences(s1, s2):
    s1_afv = avg_feature_vector(s1, model=model, num_features=300, index2word_set=index2word_set)
    s2_afv = avg_feature_vector(s2, model=model, num_features=300, index2word_set=index2word_set)
    sim = 1 - spatial.distance.cosine(s1_afv, s2_afv)
    return sim

#s1 = make_sentence(make_list('remove'))
#s2 = make_sentence(make_list('delete'))
#print(similarity_sentences(s1,s2))


def camel_to_snake(name):
    list = make_list(name)
    new_name = ""
    for w in list:
        new_name += w
        new_name += "_"
    return new_name[:-1]

def snake_to_camel(name):
    list = make_list(name)
    new_name = ""
    pp = False
    for w in list:
        c = w[0].upper() if pp else w[0].lower()
        pp = True
        new_name += c
        new_name += w[1:]
    return new_name

def change_case(name):
    if('_' in name): #this is snake
        return snake_to_camel(name)
    return camel_to_snake(name)


def find_synonyms(word):

    #dev
    return ["sum","total","append"]

    p = make_sentence(make_list(word))
    s_list = []


    #r = requests.get('https://wordsapiv1.p.mashape.com/words/'+word+'/synonyms'
    #        , headers={"x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
    #    	"x-rapidapi-key": ""} )

    #print(json.loads(r.content))
    #synonym_list = json.loads(r.content)['synonyms']

    r = requests.get('https://words.bighugelabs.com/api/2//'+word+'/json')
    j = json.loads(r.content)
    synonym_list = []
    for (key,val) in j.items():
        synonym_list += val['syn']
    #synonym_list = j['noun']['syn'] + j['verb']['syn']

    for s in synonym_list:
         if(s.count(' ')>0):
             continue
         p1 = make_sentence(make_list(s))
         sim = similarity_sentences(p,p1)
         obj = ( s, sim)
         if(not np.isnan(sim)):
             s_list.append(obj)
    #print(s_list)

    s_list.sort(key = lambda synonym: synonym[1] )
    firsts = [t[0] for t in s_list]
    return firsts[-3:]


def all_regex(regex):
    py_keywords = ['False',	'class', 'finally','is','return','None','continue','for','lambda','try','True',	'def','from','nonlocal','while','and','del','global','not',	'with','as','elif','if','or','yield','assert','else','import','pass','break','except','in','raise']
