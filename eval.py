import sys
#from search import main, findTerms



def evaluate (rlist, qrel):
    ret = len(rlist)

    relList = []
    for r in qrel:
        if qrel[r]=='1':
            relList.append(r)

    rel = len(relList)

    retrel=0
    for docno in rlist:
        if docno in qrel:
            if qrel[docno]=='1':
                retrel+=1
    
    if ret!=0 and rel!=0:
        precision = retrel/ret
        recall = retrel/rel
        return [precision, recall]
    
#if __name__ == '__main__':
#    evaluate(sys.argv)
