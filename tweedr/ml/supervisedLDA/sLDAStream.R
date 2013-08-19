require("lda")
require("pracma")

sldaModel <- readRDS("sldaModel.rds")
vocabulary <- readRDS("vocabulary.rds")

corpus <- lexicalize(tweets, lower = TRUE, vocab = vocabulary)

predictions <- slda.predict(corpus, sldaModel$topics, sldaModel$model, alpha = 1.0, eta = 0.1)
predictions <- sigmoid(predictions)
