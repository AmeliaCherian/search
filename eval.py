def main (rankList, qrels):
    numC = len(qrels)
    for x in rankList:
        if x in qrels:
            cP+=1
            qrels.pop(x)
        else:
            fP+=1
    fN+=len(qrels)
    print (cP, fP, fN)
    
