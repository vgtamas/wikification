import xml.etree.ElementTree as et
import nltk
from nltk.corpus import stopwords
import math
import operator

data = []
path = "wiki_data.xml"

context = et.iterparse(path, events=("start", "end"))

context = iter(context)

ev, root = next(context)
i = 0

articles = []
words_count = dict()
words_in_articles = dict()
stop_words = set(stopwords.words('english'))
tfidf = dict()
punctuation_mark = [',',';','!','?',':','(',')','.','[',']','{','}','<','>','=']
allowed_tags = ['VB', 'NN', 'NNS', 'NNP', 'NNPS', 'FW', 'JJ', 'VBD', 'VBP', 'CD']
top_words = dict()

test_data = []

read = 0
titles = []
base = ""
for ev, el in context:
    if read < 4500:
        if 'text' in el.tag:
            s = str(el.text)
            if 'redirect' not in s and 'REDIRECT' not in s and s != 'None':
                articles.append(s)
                words = []
                read += 1
                s = s.lower()
                tokens = nltk.word_tokenize(s)
                tokens = [w for w in tokens if w not in stop_words]
                tagged_words = nltk.pos_tag(tokens)
                for tagged_word in tagged_words:
                    if tagged_word[1] in allowed_tags and tagged_word[0] not in punctuation_mark:
                        if tagged_word[0] not in words:
                            if tagged_word[0] in words_in_articles:
                                words_in_articles[tagged_word[0]] += 1
                                words.append(tagged_word[0])
                            else:
                                words_in_articles[tagged_word[0]] = 1
                                words.append(tagged_word[0])

                        if tagged_word[0] in words_count:
                            words_count[tagged_word[0]] += 1
                        else:
                            words_count[tagged_word[0]] = 1
            root.clear()
        if 'title' in el.tag:
            titles.append(el.text)
    else:
        if read < 5000:
            if 'text' in el.tag:
                s = str(el.text)
                if 'redirect' not in s and 'REDIRECT' not in s and s != 'None':
                    test_data.append(s)
                    read += 1
        else:
            break

for article in test_data:
    words_in_artic = dict()
    s = article.lower()
    words = []
    tokens = nltk.word_tokenize(s)
    tokens = [w for w in tokens if w not in stop_words]
    tagged_words = nltk.pos_tag(tokens)
    for tagged_word in tagged_words:
        if tagged_word[1] in allowed_tags and tagged_word[0] not in punctuation_mark:
            if tagged_word[0] in words_in_artic:
                words_in_artic[tagged_word[0]] += 1
            else:
                words_in_artic[tagged_word[0]] = 1
            if tagged_word[0] not in words:
                words.append(tagged_word[0])

    for word in words:
        tfidf[word] = words_in_artic[word] * math.log(len(articles)/words_in_articles[word])


keyphrases = dict()


for article in articles:
    article = article.split(" ")
    keyphrase_in_article = []
    s = ""
    multiple_word = 0
    for word in article:
        if multiple_word:
            if "]]" in word:
                s += " " + word.replace("]]","")
                if s not in keyphrase_in_article:
                    keyphrase_in_article.append(s)
                multiple_word = 0
                s = ""
            else:
                s = word.replace("[[", "")
                multiple_word = 1
        else:
            if "[[" in word:
                if "]]" in word:
                    w = word.replace("[[","").replace("]]","")
                    if w not in keyphrase_in_article:
                        keyphrase_in_article.append(w)
                else:
                    s += word.replace("[[","")
                    multiple_word = 1

    for keyphrase in keyphrase_in_article:
        if keyphrase in keyphrases:
            keyphrases[keyphrase] += 1
        else:
            keyphrases[keyphrase] = 1

p = dict()

for word in keyphrases:
    if word in words_in_articles:
        p[word] = keyphrases[word] / words_in_articles[word]

p = sorted(p.items(), key=operator.itemgetter(1))

range = len(p) * 3//50

links = dict()
counter = 0

for x in p:
    if counter == range:
        break
    else:
        if x in titles:
            links[x] = titles[x]
            counter += 1

print('hello')



