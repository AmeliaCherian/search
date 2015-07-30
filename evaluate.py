import sys
#from search import main, findTerms

def evaluate (id, rlist, qrel):
    ret = len(rlist)

    relList = []
    for r in qrel:
        if qrel[r]=='1':
            relList.append(r)

    rel = len(relList)

    print (rlist)
    print (relList)
    if ret!=0 and rel!=0:
        retrel=0
        for docno in rlist:
            if docno in qrel:
                if qrel[docno]=='1':
                    retrel+=1
        
        precision = retrel/ret
        recall = retrel/rel
        with open ("prvalues.txt", "a") as f:
            f.write(id+' '+str(precision)+' '+str(recall)+'\n')
        return (precision, recall)
#if __name__ == '__main__':
#    evaluate(sys.argv)
