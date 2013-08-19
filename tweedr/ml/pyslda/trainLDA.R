require("lda")
corpus <- lexicalize(documents)

documents <- corpus$documents
vocabulary <- corpus$vocab

params <- sample(c(-1,1), numtopics, replace=TRUE)

result <- slda.em(documents=documents, K = numtopics, vocab=vocabulary, num.e.iterations = e_iter, num.m.iterations= m_iter, alpha = alpha, eta = eta, as.numeric(labels), params, variance = variance, lambda = lambda, logistic = logistic, method="sLDA")

topics <- result$topics
model <- result$model
saveRDS(model,model_filename)
