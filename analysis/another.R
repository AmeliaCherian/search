evaluate <- function (fqrel, fRank) {
  qrels = read.table(fqrel, sep = ' ')
  names(qrels) <- c('topic', 'x', 'docno', 'rel')
  
  
  ranks = read.table(fRank, sep = ' ')
  names(ranks)  = c('topic', 'q0', 'docno', 'rank', 'score', 'x')
  
  topicNum = unique(qrels$topic)
  for (q in topicNum) {
    print (q)
    rlist <- (subset(ranks, topic == q))$docno
    ret <- length(rlist)
    # chooses smaller between 10 and length of rank list
    k <- min(c(10, ret))
    
    relList = (subset(qrels, topic == q & rel == '1'))$docno
    
    rel <- length(relList)
    
    fP <- 0
    x <- c()
    retrel <- 0
    sumP <- 0
    p <- c()
    r <- c()
    
    # to find P@k at every point from 1 to k
    for (point in 1:k) {
      if (rlist[point] %in% relList) {
        retrel <- retrel + 1
      }
      else{
        fP <- fP + 1
      }
      
      #fN <- length(list(x for x in relList if x not in rlist))
      #tN <- numDocs - rel - fP
      
      #fPRate <- (fP / (fP + tN))
      #specificity <- (tN / (fP + tN))
      ap <- (1 / rel)
      
      precision <- retrel / (point)
      sumP <- sumP + precision
      recall <- retrel / rel
      p = c(p, precision)
      r = c(r, recall)
    }
    print (r)
    print (p)
    # makes the interpolation list
    for (some in 0:10) {
      n <- some / 10
      mx <- 0
      # goes through the recall and precision pairs
      for (l in 1:length(p)) {
        # checks if the recall value is
        # equal to a interpolation value
        if (r[l] == n) {
          mx <- p[l]
          break
        }
        # if not, gets the next max precision
        else if (r[l] > n & p[l] > mx) {
          mx <- p[l]
        }
      }
      x = c(x, mx)
    }
    b<-c(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    
    cl <- rainbow(length(topicNum))
    
    lines (b, x, 
          main = "i-Prec", xlab = "Recall", ylab = "Precision",
          type = 'o', col = cl[some+1], xlim = c(0.0, 1.0), ylim = c(0.0, 1.0))
    
    print (x)
  }
  
  
  return (sumP / k)
}
