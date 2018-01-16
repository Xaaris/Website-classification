from gensim.models import Doc2Vec
from sklearn.externals import joblib

from Download import download_html_from_url, visible_text_from_html
from Preprocess import preprocess_doc

print("Loading model")
model = Doc2Vec.load('./model/jobs.d2v')
print("Loading classifier")
classifier = joblib.load('./model/jobs_SVM.pkl')


def classify(url):
    html = download_html_from_url(url)
    print("Downloaded " + url)
    print(html)
    visible_text = visible_text_from_html(html)
    doc = preprocess_doc(visible_text)
    print("Found the following tokens")
    print(doc)
    new_vector = model.infer_vector(doc)
    classification = "No Job" if classifier.predict([new_vector])[0] < 0.5 else "Job"
    print(classification + " with confidence: " + str(classifier.decision_function([new_vector])))


url = "https://jobs.meinestadt.de/hamburg/premium?id=2709879"
classify(url)
