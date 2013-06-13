import os
import fnmatch
import csv
# import re
# import itertools
from nltk.tokenize import word_tokenize, sent_tokenize  # word_tokenize
# from collections import defaultdict  # Counter,
from sklearn import svm, metrics, neighbors, tree, naive_bayes
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import text
# pip install -e git://github.com/chbrown/scikit-text.git#egg=scikit-text
from sktext.bow import Dictionary


def iglob(pattern, root='.'):
    for parent, dirnames, filenames in os.walk(root):
        filepaths = [os.path.join(parent, filename) for filename in filenames]
        for filepath in fnmatch.filter(filepaths, pattern):
            yield filepath


info_caution = None
for filepath in iglob('**/a121571.csv'):
    info_caution = filepath
    break
else:
    print 'The required file, a121571.csv, is not in any of your subdirectories.'
    exit(1)

# choose_one:
# 137 Casualties and damage
# 436 Caution and advice
# 204 Donations of money, goods or services
#  46 People missing, found or seen
# 130 Unknown
# 280 Information source


def tokenize_sentences(sentences):
    for sentence in sent_tokenize(sentences):
        for token in word_tokenize(sentence):
            yield token


dictionary = Dictionary()
# so that no features are labeled 0 (bad for SVMlight)
dictionary.add_one('###')

# tfidf_documents = tfidf(documents, dictionary)
# index_range = range(len(dictionary.index2token))

documents = []
X = []  # except not really
Y = []
with open(info_caution) as fp:
    for row in csv.DictReader(fp):
        documents.append(row['text'])

        tokens = list(tokenize_sentences(row['text'].lower()))
        indices = dictionary.add(tokens)
        X.append(indices)
        Y.append(row['choose_one'])

# reset X
# print 'X.shape', X.shape
# shape = (rows, columns)
# raise Exception()
# gridsearch = GridSearchCV(estimator=svc, param_grid={'C': [0.1, 1.0]})

grid_CV = False
if grid_CV:
    pipeline = Pipeline([
        ('vect', text.CountVectorizer()),
        ('tfidf', text.TfidfTransformer()),
        ('clf', naive_bayes.MultinomialNB()),
    ])

    pipeline.fit(documents, Y)

    # classifier = naive_bayes.MultinomialNB()
    # classifier = tree.DecisionTreeClassifier()
    # classifier = svm.SVC()  # gamma=0.001
    # classifier = svm.LinearSVC(loss='l2', penalty='l2')
    # classifier = svm.sparse.LinearSVC()
    # classifier = neighbors.KNeighborsClassifier(3)

    # classifier.fit(train_X, train_Y)

else:
    # CountVectorizer(stop_words='english', dtype=float)
    count_vectorizer = text.CountVectorizer()
    bow = count_vectorizer.fit_transform(documents)
    bow_csr = bow.tocsr()
    tfidf_transformer = text.TfidfTransformer()
    tfidf = tfidf_transformer.fit_transform(bow_csr)

    X = tfidf
    X = X  # .toarray()  # for decision tree

    split = 0.5
    nrows = X.shape[0]
    assert nrows == len(Y), 'Data and labels must be the same length'
    split_at = int(split*nrows)

    train_X = X[split_at:]
    train_Y = Y[split_at:]

    test_X = X[:split_at]
    test_Y = Y[:split_at]

    # classifier = naive_bayes.MultinomialNB()
    # classifier = tree.DecisionTreeClassifier()
    # classifier = svm.SVC()  # gamma=0.001
    # classifier = svm.LinearSVC(loss='l2', penalty='l2')
    classifier = svm.sparse.LinearSVC()
    # classifier = neighbors.KNeighborsClassifier(3)

    classifier.fit(train_X, train_Y)

    predicted_Y = classifier.predict(test_X)
    print 'Accuracy:', metrics.accuracy_score(test_Y, predicted_Y)
    print 'P/R: %.4f/%.4f F1: %.4f' % (
        metrics.precision_score(test_Y, predicted_Y),
        metrics.recall_score(test_Y, predicted_Y),
        metrics.f1_score(test_Y, predicted_Y))
    for predicted, gold in zip(predicted_Y, test_Y)[:20]:
        print 'predicted: %s, gold: %s' % (predicted, gold)

# print metrics.classification_report(test_Y, predicted_Y)
# print metrics.confusion_matrix(test_Y, predicted_Y)

# clf.fit(X, Y)
# SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
#     gamma=0.0, kernel='rbf', max_iter=-1, probability=False, shrinking=True,
#     tol=0.001, verbose=False)
# dec = clf.decision_function([[1]])
# dec.shape[1] # 4 classes: 4*3/2 = 6
# print dictionary
