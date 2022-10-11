import pickle
import math
import nltk

def compute_prob(text, unigram_dict, bigram_dict, N, V):
    # N is the number of tokens in the training data
    # V is the vocabulary size in the training data (unique tokens)
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((n + 1) / (d + V))

    print("probability with laplace smoothing is %.5f" % p_laplace)
    return p_laplace

english_uni_dict = pickle.load(open('english_uni_dict.p', 'rb'))
english_bi_dict = pickle.load(open('english_uni_dict.p', 'rb'))

french_uni_dict = pickle.load(open('french_uni_dict.p', 'rb'))
french_bi_dict = pickle.load(open('french_uni_dict.p', 'rb'))

italian_uni_dict = pickle.load(open('italian_uni_dict.p', 'rb'))
italian_bi_dict = pickle.load(open('italian_uni_dict.p', 'rb'))

english_train = open("LangId.train.English", 'r', encoding='utf8')
french_train = open("LangId.train.French", 'r', encoding='utf8')
italian_train = open("LangId.train.Italian", 'r', encoding='utf8')

e_unigrams = word_tokenize(english_train)
f_unigrams = word_tokenize(french_train)
i_unigrams = word_tokenize(italian_train)

test_file = open("LangId.test", 'r', encoding='utf8')
test_lines = test_file.readlines()

for line in test_lines:
    english_prob = compute_prob(line, english_uni_dict, english_bi_dict, len(english_uni_dict), len(e_unigrams), len(english_uni_dict))
    french_prob = compute_prob(line, french_uni_dict, french_bi_dict, len(french_uni_dict), len(f_unigrams), len(french_uni_dict))
    italian_prob = compute_prob(line, italian_uni_dict, italian_bi_dict, len(italian_uni_dict), len(i_unigrams), len(i_uni_dict))
