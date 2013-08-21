### Supervised Latent Dirchlet Allocation

This sub-module creates a python wrapper for the sLDA algorithm in R for binary classification and topic modeling. This wrapper implements methods in a fashion similar to classifiers provided in Scikit-Learn. Because there is no way to convert the R "slda" model into a Python object, the model is stored on disk. The sLDA classifier cannot currently handle non-ASCII text.

* * *

To create a sLDA classifier object, call supervisedLDA() and provide a filename for where you want the model to be saved.

Methods:

1.  Fit(documents, labels): Trains the sLDA classifier using the provided corpus and corresponding labels.
2.  Predict(Document, gold_labels): Returns a vector containing the likelihood that each document in testing corpus will have a positive label.
3.  SaveModel: Saves the vocabulary used in the trained sLDA model.
4.  LoadModel: Loads an existing vocabulary into the sLDA model.