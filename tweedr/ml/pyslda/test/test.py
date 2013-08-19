from PySLDA import supervisedLDA
from nltk.corpus import inaugural
import random
from string import punctuation


testModel = supervisedLDA()
inaugural_text = inaugural.raw()
inaugural_text = inaugural_text.split("\n\n")
inaugural_text = map(lambda x: x.translate(None, "\n").translate(None, punctuation).lower().strip(), inaugural_text)
num_texts = len(inaugural_text)
labels = []
for i in range(num_texts):
    labels.append(random.random())
labels = map(lambda x: x >= 0.5, labels)
del inaugural_text[1338]
del labels[1338]
testModel.train(inaugural_text, labels)
