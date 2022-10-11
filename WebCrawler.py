import re
import requests
import math
import nltk
import pickle
import urllib.request
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from os import path

# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'meta']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    elif element.parent.name in ['div']:
        return (('div' or '<a') not in str(element))
    elif element.parent.name in ['body']:
        return ('script src' not in str(element))
    return True

def create_tfidf(tf, idf):
    tf_idf = {}
    for t in tf.keys():
        tf_idf[t] = tf[t] * idf[t]

    return tf_idf

def create_tf_dict(tokens):
    tf_dict = {}
    # get term frequencies
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # get term frequencies in a more Pythonic way
    token_set = set(tokens)
    tf_dict = {t: tokens.count(t) for t in token_set}

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    return tf_dict

#Url regarding bonsai trees
starter_url = 'https://en.wikipedia.org/wiki/Bonsai'
r = requests.get(starter_url)
data = r.text
soup = BeautifulSoup(data, features="html.parser")

# write urls to a file
with open('urls.txt', 'w') as f:
    for link in soup.find_all('a'):
        link_str = str(link.get('href'))
        if 'Bonsai' in link_str or 'bonsai' in link_str:
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' and 'https://archive.org' not in link_str:
                f.write(link_str + '\n')

with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()

counter = 1
urlfile = open('urls.txt', 'r')
urls = urlfile.readlines()

#Check every url and create a file for each page's text
for u in urls:
    #print(u.strip())
    try:
        html = urllib.request.urlopen(u.strip())
        soup = BeautifulSoup(html, features="html.parser")
        data = soup.findAll(text=True)
        result = filter(visible, data)
        temp_list = list(result)      # list from filter
        temp_str = ' '.join(temp_list)
        temp_str = ' '.join(temp_str.split())
        with open('scraped_file{}.txt'.format(counter), 'w', encoding='utf-8') as f:
            f.writelines(temp_str)
            counter+=1
    except:
        print("Invalid URL, Skipped.")

#Create files with sentences split
i = 1
while path.exists('scraped_file{}.txt'.format(i)):
        f = open('scraped_file{}.txt'.format(i), 'r', encoding='utf-8')
        newF = open('sent_file{}.txt'.format(i), 'w', encoding='utf-8')
        text = f.read()
        sentences = sent_tokenize(text)
        for sentence in sentences:
            newF.write(sentence+'\n')
        i+=1

#Lowercase and remove stopwords and add everything useful to total_tokens
total_tokens = []
fileNum = 1
stopwords = stopwords.words('english')
while path.exists('sent_file{}.txt'.format(fileNum)):
    f = open('sent_file{}.txt'.format(fileNum), 'r', encoding='utf-8')
    tokens = [t.lower() for t in word_tokenize(f.read()) if t.isalpha()]
    tokens_content = [t for t in tokens if t not in stopwords]
    total_tokens.extend(tokens_content)
    fileNum+=1

tf_bonsai = create_tf_dict(total_tokens)
vocab = set(tf_bonsai.keys())

# find the highest tf-idf terms for each document
bonsai_term_weights = sorted(tf_bonsai.items(), key=lambda x:x[1], reverse=True)
print("\nMost Common: ", bonsai_term_weights[:40])

#Will manually select top 10 terms: bonsai, tree, die, time, japan, soil, water, size, trunk, art
#From 40 terms found above


topterms = {"bonsai", "tree", "die", "time", "japan", "soil", "water", "size", "trunk", "art"}
knowledge_base = {}

for term in topterms:
    newList = []
    num = 1
    while path.exists('sent_file{}.txt'.format(num)):
        f = open('sent_file{}.txt'.format(num), 'r', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            if term in line:
                newList.append(line)
        num += 1
    knowledge_base[term] = newList
for key, value in knowledge_base.items():
    print(key, ' : ', value)
    print('\n'+ '\n'+ '\n')
pickle.dump(knowledge_base, open('knowledge_base.p', 'wb'))  # write binary

