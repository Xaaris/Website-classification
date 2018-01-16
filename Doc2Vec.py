from gensim.models import Doc2Vec

from LabledLineSentence import LabeledLineSentence


def build_doc2vec_model():
    print("Getting sources...")
    path_neg = "./data/negative/"
    path_pos = "./data/positive/"
    path_model = "./model/jobs.d2v"
    sources = {path_neg + "jobs_neg_test_5k.txt": "TEST_NEG", path_pos + "jobs_pos_test_5k.txt": "TEST_POS",
               path_neg + "jobs_neg_train_20k.txt": "TRAIN_NEG", path_pos + "jobs_pos_train_20k.txt": "TRAIN_POS"}
    sentences = LabeledLineSentence(sources)
    print("Total number of docs: " + str(len(sentences.to_array())))

    model = Doc2Vec(min_count=1, window=10, size=400, sample=1e-4, negative=5, workers=8)
    model.build_vocab(sentences.to_array())
    print("vocabulary set")

    for epoch in range(20):
        print("Starting epoch " + str(epoch))
        model.train(sentences.sentences_perm(), total_examples=model.corpus_count, epochs=model.iter)

    model.save(path_model)
    print("model saved under " + path_model)


def model_test():
    model = Doc2Vec.load('./model/jobs.d2v')
    test_word = "frau"
    print("Most similar to " + test_word + " is: " + str(model.most_similar(test_word)))


model_test()
