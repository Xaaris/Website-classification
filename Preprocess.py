import glob

from nltk.corpus import stopwords
from nltk.stem.snowball import GermanStemmer


def remove_stop_words(words):
    return [word for word in words if word not in stopwords.words('german')]


def remove_punctuation(words):
    return [''.join(char for char in word if char not in ['.', '"', ',', '(', ')', '!', '?', ';', ':', 'ǀ', '+']) for
            word in words]


def remove_short_words_and_numbers(words):
    return [word for word in words if len(word) > 2 and not word.isdigit()]


def apply_stemming(words):
    stemmer = GermanStemmer()
    return [stemmer.stem(word) for word in words]


def preprocess_doc(words):
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

# docs_en = []
# docs_de = []
# file_names = get_file_names_from_directory("/Users/hannes/Desktop/jobNoJob-master/files/positives/raw/", "html")
# for file_name in file_names:
#     html = read_file_from_disc(file_name)
#     visible_text = text_from_html(html)
#     if len(visible_text) > 0:
#         try:
#             language = detect(" ".join(visible_text))
#             print(language)
#         except lang_detect_exception.LangDetectException as error:
#             print(error)
#         processed_words = preprocess_doc(html)
#         if language == "de":
#             docs_de.append(processed_words)
#         if language == "en":
#             docs_en.append(processed_words)
# write_docs_to_disc("jobs-pos_de.txt", docs_de)
# write_docs_to_disc("jobs-pos_en.txt", docs_en)


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
