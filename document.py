from os import listdir
from os.path import isfile, join
from nltk import word_tokenize
import string



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

