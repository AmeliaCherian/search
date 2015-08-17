graphing <-function(l){
mydata <- read.csv("~/Documents/search/iprec.txt", header = TRUE, sep = " ")
names(mydata) = c('topicnumber', 'recall', 'precision')

sample <- as.numeric(mydata$topicnumber)
hello <- c()
for (num in l){
  hello <- c(hello, subset(mydata, topicnumber==num))}

cl <- rainbow(length(l))

plot (hello[2]$recall, hello[3]$precision, main = "i-Prec", xlab = "Recall", ylab = "Precision", type = 'o', col = cl[1], xlim = c(0.0, 1.0), ylim = c(0.0, 1.0))

for (counter in 4:length(hello)){
    lines(hello[counter+1]$recall, hello[counter+2]$precision, col=cl[(counter+2)/3], type = 'o')}

legend("topleft", legend = l, col=cl[1:length(l)], pch=1) 

}

