require("lda")
require("pracma")

sldaModel <- readRDS(model_filename)

corpus <- lexicalize(testDocuments, lower=TRUE, vocab=vocabulary)

predictions <- slda.predict(corpus, topics, sldaModel, alpha = alpha, eta = eta)
predictions <- sigmoid(predictions)