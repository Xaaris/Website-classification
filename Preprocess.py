import glob
import threading
import time
import unicodedata
from multiprocessing import Process

from langdetect import detect, lang_detect_exception
from nltk.corpus import stopwords
from nltk.stem.snowball import GermanStemmer


def remove_punctuation(word):
    punctuation = {'.', '"', ',', '(', ')', '!', '?', ';', ':', 'ǀ', '+', '|', '*', '[', ']', '{', '}', '\''}
    return ''.join(char for char in word if char not in punctuation and unicodedata.category(char)[0] != "C")


def is_short_word(word):
    return len(word) < 2


def is_number(word):
    return word.isdigit()


def apply_stemming(word):
    return stemmer.stem(word)


def is_stopword(word):
    return word in cachedStopWords


def lang_detect_and_preprocess(lines_of_text):
    local_docs = []
    for i, line in enumerate(lines_of_text):
        if len(line) > 0:
            try:
                language = detect(line)
                print(str(i) + " " + language)
                if language == "de":
                    processed_words = preprocess_doc(line.split())
                    local_docs.append(" ".join(processed_words))
            except lang_detect_exception.LangDetectException as error:
                print(error)

    threadLock.acquire()
    for line in local_docs:
        append_line_to_file(save_path, line)
    threadLock.release()


def preprocess_doc(words):
    processed_text = []
    for word in words:
        clean_word = remove_punctuation(word)
        if not is_short_word(clean_word) and not is_number(clean_word) and not is_stopword(clean_word):
            processed_text.append(apply_stemming(clean_word))
    return processed_text


def write_docs_to_disc(filename, docs):
    with open(filename, 'w') as docs_file:
        for doc in docs:
            for word in doc:
                docs_file.write(word + " ")
            docs_file.write("\n")


def append_line_to_file(filename, line):
    with open(filename, 'a') as file:
        file.write(line + "\n")


def read_lines_from_file(filename):
    lines = []
    with open(filename, "r") as file:
        for line in file:
            line = bytes(line, 'utf-8').decode('utf-8', 'ignore')
            lines.append(line)
    return lines


def get_file_names_from_directory(path, ending):
    return glob.glob(path + "*." + ending)


def read_file_from_disc(path):
    print("attempting to read " + path)
    file = open(path, 'rb')
    return file.read()


def chunk(url_list, number_of_chunks):
    length_of_list = len(url_list)
    assert 0 < number_of_chunks <= length_of_list
    chunk_size = (length_of_list // number_of_chunks) + 1
    return [url_list[p:p + chunk_size] for p in range(0, length_of_list, chunk_size)]


# caching
detect("this is just for loading")
cachedStopWords = stopwords.words('german')

threadLock = threading.Lock()
stemmer = GermanStemmer()

load_path = "./data/positive/visible_text/successful_text_extractions.txt"
save_path = "./data/positive/visible_text/preprocessed_text.txt"


# start = time.time()
# print("STARTED!")
#
# number_of_processes = 8
#
# lines = read_lines_from_file(load_path)
# chunks = chunk(lines, number_of_processes)
#
# processes = []
# if __name__ == '__main__':
#     for i in range(number_of_processes):
#         process = Process(target=lang_detect_and_preprocess, args=(chunks[i],))
#         process.start()
#         processes.append(process)
#     for t in processes:
#         t.join()
#
# end = time.time()
# print("DONE")
# print("Time: " + str(end - start))

# nltk.download('stopwords')
