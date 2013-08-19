require("lda")
model <- readRDS(model_filename)
vocab <- readRDS(vocab_filename)
topics <- readRDS(topics_filename)