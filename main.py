import xml.etree.ElementTree as et
import nltk
from nltk.corpus import stopwords
import math

data = []
path = "wiki_data.xml"

# get an iterable
context = et.iterparse(path, events=("start", "end"))

# turn it into an iterator
context = iter(context)

# get the root element
ev, root = next(context)
i = 0

articles = []
words_count = dict()
words_in_articles = dict()
stop_words = set(stopwords.words('english'))
tfidf = dict()
punctuation_mark = [',',';','!','?',':','(',')','.','[',']','{','}','<','>','=']
allowed_tags = ['VB', 'NN', 'NNS', 'NNP', 'NNPS', 'FW', 'JJ', 'VBD', 'VBP']
top_words = dict()

read = 0

for ev, el in context:
    if read < 5000:
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
    else:
        break


for article in articles:
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

    tfidf_in_doc = dict()
    for word in words_in_artic:
        tfidf_in_doc[word] = tfidf[word]

    tfidf_in_doc = dict(sorted(tfidf_in_doc.items(), key=lambda item: item[1],reverse=True))

    counter = len(tfidf) * 3 // 50

    for x in list(tfidf_in_doc.items())[:counter]:
        if x[0] in top_words:
            top_words[x[0]] += 1
        else:
            top_words[x[0]] = 1

keyphrases = dict()

for word in top_words:
        keyphrases[word] = top_words[word] / words_in_articles[word]

for word in keyphrases:
    if word in tfidf:
        print(keyphrases[word],tfidf[word]  )
