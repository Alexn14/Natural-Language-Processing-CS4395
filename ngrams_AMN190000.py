import nltk
import pickle
from nltk import word_tokenize
def readfile(file_name):
    f = open(file_name, 'r', encoding='utf8')
    text = (f.read()).strip()
    unigrams = word_tokenize(text)
    bigrams = [(unigrams[k], unigrams[k+1]) for k in range(len(unigrams)-1)]
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}
    return unigram_dict, bigram_dict

english_unigram_dict, english_bigram_dict = readfile("LangId.train.English")
french_unigram_dict, french_bigram_dict = readfile("LangId.train.French")
italian_unigram_dict, italian_bigram_dict = readfile("LangId.train.Italian")

pickle.dump(english_unigram_dict, open('english_uni_dict.p', 'wb'))
pickle.dump(english_bigram_dict, open('english_bi_dict.p', 'wb'))

pickle.dump(french_unigram_dict, open('french_uni_dict.p', 'wb'))
pickle.dump(french_bigram_dict, open('french_bi_dict.p', 'wb'))

pickle.dump(italian_unigram_dict, open('italian_uni_dict.p', 'wb'))
pickle.dump(italian_bigram_dict, open('italian_bi_dict.p', 'wb'))