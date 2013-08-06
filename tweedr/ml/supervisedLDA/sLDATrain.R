require("lda")
corpus <- lexicalize(input, lower = TRUE)
documents <- corpus$documents
vocab <- corpus$vocab

numptopics <- 5
params <- sample(c(-1,1),numptopics,replace=TRUE)

result <- slda.em(documents=documents,K=numtopics,vocab=vocab,num.e.iterations=10,num.m.iterations=4,alpha=1.0, eta=0.1,labels,params, variance=0.25,lambda=1.0,logistic=FALSE,method="sLDA")

saveRDS(result, "sldaModel.rds")
saveRDS(vocab, "vocabulary.rds")