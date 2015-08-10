import sys
#from search import main, findTerms

def evaluate (id, rlist, qrel, numDocs):
    ret = len(rlist)

    relList = []
    for r in qrel:
        if qrel[r]=='1':
            relList.append(r)

    rel = len(relList)

    #print (rlist)
    print (relList)

    fP = 0
    if ret!=0 and rel!=0:
        retrel=0
        for docno in rlist:
            if docno in relList:
                retrel+=1
            else:
                fP +=1
        fN = len(list(x for x in relList if x not in rlist))
        tN = numDocs - rel - fP

        fPRate = (fP/(fP+tN))
        specificity =  (tN/(fP+tN))
        
        
        precision = retrel/ret
        recall = retrel/rel
        with open ("prvalues.txt", "a") as f:
            f.write(id+' '+str(precision)+' '+str(recall)+'\n')
        return (precision, recall)
