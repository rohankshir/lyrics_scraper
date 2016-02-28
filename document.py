from os import listdir
from os.path import isfile, join
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import string

stemmer = PorterStemmer()

more_stop_words = set()
more_stop_words.add("yeah")
more_stop_words.add("like")
more_stop_words.add("just")
more_stop_words.add("know")
more_stop_words.add("want")
more_stop_words.add("need")
more_stop_words.add("got")
more_stop_words.add("make")
more_stop_words.add("wanna")
more_stop_words.add("gonna")
more_stop_words.add("gotta")
more_stop_words.add("tryna")
more_stop_words.add("told")
more_stop_words.add("this")
more_stop_words.add("maybe")
more_stop_words.add("cause")
more_stop_words.add("nigga")
more_stop_words.add("niggas")
more_stop_words.add("used")

def get_document(filepath):
    with open(filepath, 'r') as f:
        return f.read()
    return ""

def filter_word(word):
    if len(word) <= 3:
        return False
    for i in word:
        if not i.isalpha():
            return False
    return word not in more_stop_words
    

def filter_words(line):
    words = line.split()
    words = filter(filter_word, words)
    return " ".join(words)


def read_documents(directory):
    return [get_relevant_lyrics(get_document(join(directory, f))) for f in listdir(directory) if isfile(join(directory, f))]
    w

#  Words are cleaned by finding repeated sequences of three or more
# characters and reducing them to two. For example, "looooveeee" will
# be shortened to "loovee". This will also lowercase every word and stem. "Running" will become "run"
def clean_word(word):

    if not word:
        return ""
    word = word.lower()
    
    count = 0
    last_char = word[0]
    result = ""

    for i in range(len(word)):
        curr_char = word[i]
        if curr_char == last_char:
            count+= 1
        else:
            count = 1

        if count < 3:
            result += curr_char
            
        last_char = curr_char

    return result

    
def preprocess_word(s):
    exclude = set(string.punctuation)
    s = s.decode("ascii","ignore")
    s = ''.join(ch for ch in s.lower() if ch not in exclude)
    s = s.lower()
    try:
        s = stemmer.stem(s)
    except:
        pass
    return clean_word(s)

def filter_and_preprocess_words(line):
    words = line.split()
    words = filter(filter_word, words)
    clean_words = map(preprocess_word, words)
    clean_words = filter(filter_word, clean_words)
    return " ".join(clean_words)

def get_relevant_lyrics(document_s):
    lines = document_s.split('\n')
    lines = lines[:-1] #remove last line

    def filter_line(line):
        if line.isspace() or (line and line[0] == '['):
            return False
        return True

    filtered = filter (filter_line, lines)
    
    return filter_and_preprocess_words(" ".join(filtered))

