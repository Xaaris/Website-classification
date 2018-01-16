import numpy
from gensim.models import Doc2Vec
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import classification_report


def build_classifier():
    print("Loading Model")
    model = Doc2Vec.load('./model/jobs.d2v')

    number_of_positives = 20000
    number_of_negatives = 20000
    total_number_of_jobs = number_of_positives + number_of_negatives
    train_array = numpy.zeros((total_number_of_jobs, 400))
    train_labels = numpy.zeros(total_number_of_jobs)
    for i in range(number_of_positives):
        prefix_train_pos = 'TRAIN_POS_' + str(i)
        train_array[i] = model.docvecs[prefix_train_pos]
        train_labels[i] = 1
    for i in range(number_of_negatives):
        prefix_train_neg = 'TRAIN_NEG_' + str(i)
        train_array[number_of_positives + i] = model.docvecs[prefix_train_neg]
        train_labels[number_of_positives + i] = 0

    number_of_test_positives = 5000
    number_of_test_negatives = 5000
    total_number_of_test_jobs = number_of_test_positives + number_of_test_negatives
    test_array = numpy.zeros((total_number_of_test_jobs, 400))
    test_labels = numpy.zeros(total_number_of_test_jobs)
    for i in range(number_of_test_positives):
        prefix_test_pos = 'TEST_POS_' + str(i)
        test_array[i] = model.docvecs[prefix_test_pos]
        test_labels[i] = 1
    for i in range(number_of_test_negatives):
        prefix_test_neg = 'TEST_NEG_' + str(i)
        test_array[number_of_test_positives + i] = model.docvecs[prefix_test_neg]
        test_labels[number_of_test_positives + i] = 0

    print("Fitting the classifier")
    # classifier = LogisticRegression()
    # classifier = svm.SVC()
    classifier = svm.LinearSVC()
    classifier.fit(train_array, train_labels)

    predictions = classifier.predict(test_array)
    target_names = ['class 0', 'class 1']
    print(classification_report(test_labels, predictions, target_names=target_names))

    path_classifier = "./model/jobs_LinearSVM.pkl"
    joblib.dump(classifier, path_classifier)
    print("Classifier saved as " + path_classifier)
