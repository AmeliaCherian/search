graphing <- function(){#l) {
  mydata <- read.csv("~/Documents/search/iprec.txt", header = FALSE, sep = " ")
  names(mydata) = c('topicnumber', 'recall', 'precision')
  l = unique(mydata$topicnum)
  
  plot(NULL, xlim = c(0.0, 1.0), ylim = c(0.0, 1.0), main = "i-Prec", xlab = "Recall", ylab = "Precision")
  r<-c(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
  #p<-c()
  counter = 0
  
  cl <- rainbow(length(l))
  
  for (num in l) {
    counter = counter+1
    p <- subset(mydata, topicnumber == num)$precision
    print (subset(mydata, topicnumber == num))
    lines(r, p,col = cl[(counter)], type = 'o')
  }
  
  #legend("bottomright", legend = l, col = cl[1:length(l)], pch = 1)
  
}