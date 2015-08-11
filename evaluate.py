import sys
#from search import main, findTerms

def evaluate (id, rlist, qrel, numDocs):
    ret = len(rlist)
    k = min(10, ret)
    
    relList = []
    for r in qrel:
        if qrel[r]=='1':
            relList.append(r)

    rel = len(relList)
    print (relList)

    fP = 0
    x =[]
    retrel=0
    sumP = 0
    data = []
    
    for blank in range(k):
        if rlist[blank] in relList:
            retrel+=1
        else:
            fP +=1
                
        fN = len(list(x for x in relList if x not in rlist))
        tN = numDocs - rel - fP

        fPRate = (fP/(fP+tN))
        specificity =  (tN/(fP+tN))
        ap = (1/rel)
        
        precision = retrel/(blank+1)
        sumP += precision
        recall = retrel/rel
        
        data.append([precision, recall])
        
    with open ('prvalues.txt', 'a') as f:
        for x in data:
            f.write (id + str(x[0]) + str(x[1]))
        
    return sumP/k
