require("lda")
corpus <- lexicalize(tweets, lower = TRUE)

documents <- corpus$documents
vocabulary <- corpus$vocab

numtopics <- 5
params <- sample(c(-1,1),numtopics,replace=TRUE)

result <- slda.em(documents=documents,K=numtopics,vocab=vocabulary,num.e.iterations=10,num.m.iterations=4,alpha=1.0, eta=0.1,labels,params, variance=0.25,lambda=1.0,logistic=TRUE,method="sLDA")

saveRDS(result, file="sldaModel.rds")
saveRDS(vocabulary, file="vocabulary.rds")

