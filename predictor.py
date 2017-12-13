from gensim.models import doc2vec
from download_and_preprocess import download_html_from_url, preprocess_doc

model = doc2vec.Doc2Vec.load("model")

url = "https://wpjobs.blob.core.windows.net/3760-xingag/2ljQ65/anzeige.html"
html = download_html_from_url(url)
doc = preprocess_doc(html)
# doc = ["hallo", "dies", "ist", "ein", "test"]
new_vector = model.infer_vector(doc)
sims = model.docvecs.most_similar([new_vector]) #gives you top 10 document tags and their cosine similarity
print(sims)
# for vec in model.docvecs:
#     print(vec)