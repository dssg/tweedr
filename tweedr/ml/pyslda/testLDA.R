require("lda")
require("pracma")


sldaModel <- readRDS(model_filename)
corpus <- lexicalize(testDocuments, lower=TRUE, vocab=vocabulary)
pred <- slda.predict(corpus, sldaModel$topics, sldaModel$model, alpha = 1.0, eta = 0.1)

pred <- sigmoid(pred)