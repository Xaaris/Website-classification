# gensim modules
# random
from random import shuffle

# numpy
import numpy
from gensim import utils
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
# classifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm

from download_and_preprocess import download_html_from_url, preprocess_doc


class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


# sources = {'jobs-test-neg.txt':'TEST_NEG', 'jobs-test-pos.txt':'TEST_POS', 'jobs-train-neg.txt':'TRAIN_NEG', 'jobs-train-pos.txt':'TRAIN_POS'}
# sources = {'./data/negative/preprocessed/jobs-neg_de.txt':'TRAIN_NEG', './data/positive/preprocessed/jobs-pos_de.txt':'TRAIN_POS'}
# sentences = LabeledLineSentence(sources)
# print(len(sentences.to_array()))
# model = Doc2Vec(min_count=1, window=10, size=400, sample=1e-4, negative=5, workers=8)
# model.build_vocab(sentences.to_array())
# print("vocabulary set")

# for epoch in range(20):
#     print("and another epoch")
#     model.train(sentences.sentences_perm(), total_examples=model.corpus_count, epochs=model.iter)
#
# model.save('./model/jobs_no_validation.d2v')
# print("model saved")
model = Doc2Vec.load('./model/jobs_no_validation.d2v')

# print(model.most_similar('w/m'))


number_of_positives = 1879
number_of_negatives = 1557
total_number_of_jobs = number_of_positives + number_of_negatives
train_arrays = numpy.zeros((total_number_of_jobs, 400))
train_labels = numpy.zeros(total_number_of_jobs)
for i in range(number_of_positives):
    prefix_train_pos = 'TRAIN_POS_' + str(i)
    train_arrays[i] = model.docvecs[prefix_train_pos]
    train_labels[i] = 1
for i in range(number_of_negatives):
    prefix_train_neg = 'TRAIN_NEG_' + str(i)
    train_arrays[number_of_positives + i] = model.docvecs[prefix_train_neg]
    train_labels[number_of_positives + i] = 0



# test_arrays = numpy.zeros((1600, 100))
# test_labels = numpy.zeros(1600)
# for i in range(800):
#     prefix_test_pos = 'TEST_POS_' + str(i)
#     prefix_test_neg = 'TEST_NEG_' + str(i)
#     test_arrays[i] = model.docvecs[prefix_test_pos]
#     test_arrays[800 + i] = model.docvecs[prefix_test_neg]
#     test_labels[i] = 1
#     test_labels[800 + i] = 0

# classifier = LogisticRegression()
# classifier.fit(train_arrays, train_labels)

classifier = svm.SVC()
classifier.fit(train_arrays, train_labels)

# print(classifier.score(test_arrays, test_labels))

url = "http://scikit-learn.org/stable/modules/svm.html"
html = download_html_from_url(url)
print(html)
doc = preprocess_doc(html)
print(doc)
new_vector = model.infer_vector(doc)
classification = "No Job" if classifier.predict([new_vector])[0] < 0.5 else "Job"
print(classifier.predict([new_vector])[0])
print(classification + " with confidence: " + str(classifier.decision_function([new_vector])))


