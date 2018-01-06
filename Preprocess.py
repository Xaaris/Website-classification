import glob

from langdetect import detect, lang_detect_exception
from nltk.corpus import stopwords
from nltk.stem.snowball import GermanStemmer


def remove_punctuation(word):
    return ''.join(char for char in word if char not in ['.', '"', ',', '(', ')', '!', '?', ';', ':', 'ǀ', '+'])


def is_short_word(word):
    return len(word) > 2


def is_number(word):
    return word.isdigit()


def apply_stemming(word):
    return stemmer.stem(word)


def is_stopword(word):
    return word in stopwords.words('german')


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
    with open(filename) as file:
        return file.readlines()


def get_file_names_from_directory(path, ending):
    return glob.glob(path + "*." + ending)


def read_file_from_disc(path):
    print("attempting to read " + path)
    file = open(path, 'rb')
    return file.read()


docs_de = []
load_path = "./data/negative/visible_text/successful_text_extractions.txt"
save_path = "./data/negative/visible_text/preprocessed_text.txt"
stemmer = GermanStemmer()
for i, line in enumerate(read_lines_from_file(load_path)):
    if len(line) > 0:
        try:
            language = detect(line)
            print(str(i) + " " + language + ": " + line)
            if language == "de":
                processed_words = preprocess_doc(line.split())
                docs_de.append(processed_words)
        except lang_detect_exception.LangDetectException as error:
            print(error)

write_docs_to_disc(save_path, docs_de)

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
