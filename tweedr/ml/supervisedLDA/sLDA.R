require(lda)
documents <- read.documents(filename = tweetFile)
vocab <- read.vocab(filename = vocabFile)
scores <- read.table(labelFile, header = FALSE)
scores <- scores$V1

cutoff <- round(cutoff*length(documents))
Xtrain <- documents[1:cutoff]
Xtest <- documents[cutoff:length(documents)]
Ytrain <- scores[1:cutoff]
Ytest <- scores[cutoff:length(documents)]

numtopics <- 6
params <- sample(c(-1,1), numtopics, replace=TRUE)

result <- slda.em(documents=Xtrain,K=numtopics,vocab=vocab,num.e.iterations=10,num.m.iterations=4,alpha=1.0, eta=0.1,Ytrain,params, variance=0.25,lambda=1.0,logistic=FALSE,method="sLDA")

#Make a pretty picture
require(ggplot2)
Topics <- apply(top.topic.words(result$topics, 5, by.score = TRUE), 2, paste, collapse=" ")

all_topics <- result$topics

coefs <- data.frame(coef(summary(result$model)))

theme_set(theme_bw())

coefs <- cbind(coefs, Topics=factor(Topics, Topics[order(coefs$Estimate)]))

coefs <- coefs[order(coefs$Estimate),]

#qplot(Topics, Estimate, colour=Estimate, size = abs(t.value), data=coefs) + geom_errorbar(width=0.5, aes(ymin=Estimate-Std..Error,ymax=Estimate+Std..Error)) +coord_flip() + xlab("Words/Topics")+ylab("Casuality/Damage") + ggtitle("Supervised LDA to identify words that indicate Casualties/Damage")

predictions <- slda.predict(Xtest,result$topics,result$model, alpha = 1.0, eta= 0.1)