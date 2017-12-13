from gensim.models.doc2vec import Doc2Vec, TaggedDocument


def write_docs_to_disc(filename, docs):
    with open(filename, 'w') as docs_file:
        for doc in docs:
            for word in doc:
                docs_file.write(word + " ")
            docs_file.write("\n")


def read_lines_from_file(filename):
    with open(filename) as file:
        return file.readlines()


docs = read_lines_from_file("docs.txt")

tagged_docs = []
for i, text in enumerate(docs):
    tagged_docs.append(TaggedDocument(text, [i]))

print(tagged_docs)

# model = Doc2Vec(tagged_docs, size=100, window=300, min_count=1, workers=4)
model = Doc2Vec(size=100, alpha=0.025, min_alpha=0.025, min_count=1, dm=0)  # use fixed learning rate
model.build_vocab(tagged_docs)

for epoch in range(10):
    model.train(tagged_docs, total_examples=model.corpus_count, epochs=model.iter)
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save("model")

for vec in model.docvecs:
    print(vec)
