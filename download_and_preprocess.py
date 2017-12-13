import urllib.request
import urllib.error

import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import GermanStemmer
import glob


def text_from_html(body):
    if body is None:
        return []
    soup = BeautifulSoup(body, 'html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    return soup.get_text(strip=False).split()


def download_html_from_url(url):
    try:
        with urllib.request.urlopen(url) as url:
            return url.read()
    except urllib.error.HTTPError as err:
        if err.code != 404:
            raise


def remove_stop_words(words):
    return [word for word in words if word not in stopwords.words('german')]


def remove_punctuation(words):
    return [''.join(char for char in word if char not in ['.', '"', ',', '(', ')', '!', '?', ';', ':', 'ǀ', '+']) for word in words]


def remove_short_words_and_numbers(words):
    return [word for word in words if len(word) > 2 and not word.isdigit()]


def apply_stemming(words):
    stemmer = GermanStemmer()
    return [stemmer.stem(word) for word in words]


def preprocess_doc(html_doc):
    words = text_from_html(html_doc)
    return apply_stemming(remove_short_words_and_numbers(remove_punctuation(remove_stop_words(words))))


def write_docs_to_disc(filename, docs):
    with open(filename, 'w') as docs_file:
        for doc in docs:
            for word in doc:
                docs_file.write(word + " ")
            docs_file.write("\n")


def read_lines_from_file(filename):
    with open(filename) as file:
        return file.readlines()


def get_file_names_from_directory(path, ending):
    return glob.glob(path + "*." + ending)


def read_file_from_disc(path):
    print("attempting to read " + path)
    file = open(path, 'rb')
    return file.read()


# docs = []
# file_names = get_file_names_from_directory("/Users/hannes/Desktop/jobNoJob-master/files/negatives/raw/", "html")
# for file_name in file_names:
#     html = read_file_from_disc(file_name)
#     processed_words = preprocess_doc(html)
#     print(str(len(processed_words)) + " " + str(processed_words))
#     docs.append(processed_words)
#
# write_docs_to_disc("jobs-neg.txt", docs)


# nltk.download('stopwords')
# url_list = read_lines_from_file("urls.txt")
#
# docs = []
# for url in url_list:
#     html = download_html_from_url(url)
#     processed_words = preprocess_doc(html)
#     print(str(len(processed_words)) + " " + str(processed_words))
#     docs.append(processed_words)
#
# write_docs_to_disc("docs.txt", docs)