#!/Users/rohan/miniconda/bin/python
# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import CountVectorizer
from os import listdir
from os.path import isfile, join
from nltk import word_tokenize
import string
import lda
import numpy as np
from nltk.corpus import stopwords

def get_document(filepath):
    with open(filepath, 'r') as f:
        return f.read()
    return ""



def get_relevant_lyrics(document_s):
    lines = document_s.split('\n')
    lines = lines[:-1] #remove last line

    def filter_line(line):
        if line.isspace() or (line and line[0] == '['):
            return False
        return True

    filtered = filter (filter_line, lines)

    return " ".join(filtered)

def read_documents(directory):
    return [get_relevant_lyrics(get_document(join(directory, f))) for f in listdir(directory) if isfile(join(directory, f))]
    
def preprocess_word(s):
    exclude = set(string.punctuation)
    s = ''.join(ch for ch in s.lower() if ch not in exclude)
    return s.lower()


def lda_lda(docs, num_topics, num_iters, n_top_words):
    vec = CountVectorizer(tokenizer=word_tokenize,
                          stop_words='english',
                          preprocessor=preprocess_word,
                          lowercase=True)
    data = vec.fit_transform(docs)
    vocab = vec.get_feature_names()
    model = lda.LDA(n_topics=num_topics, n_iter=num_iters, random_state=1)
    model.fit(data)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works

    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]

        s = u'Topic {}: {}'.format(i, u' '.join(topic_words)).encode('utf-8').strip()
        print s


def gensim_lda(docs, num_topics, num_iters, num_top_words ):

    texts = []
    en_stop = stopwords.words('english')
    for i in docs:
        tokens = word_tokenize(preprocess_word(i))

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
    
        # process tokens
        processed_tokens = [preprocess_word(i) for i in stopped_tokens]
    
        # add tokens to list
        texts.append(processed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
        
    # generate LDA model
    ldamodel = models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary, passes=num_iters)
    ldamodel.print_topics(num_topics)

    
def main():
    docs = read_documents('/Users/rohan/Projects/LyricsAnalysis/r-b-hip-hop-songs/2000/')
    gensim_lda(docs, 10, 1000, 10)
    #lda_lda(docs, 10, 1000, 10)

    

#    print vec.get_feature_names()

    


if __name__ == "__main__":
    main()

