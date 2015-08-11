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
        
        data.append([recall, precision])
    
    ps = {thing[0]:thing[1] for thing in data}
    for some in range(0, 11):
        n = some/10
        max = 0
        for l in ps:
            print (n, l, ps[l])
            if l==n:
                max = ps[l]
                break
            elif l>n and ps[l]>max:
                max = ps[l]
        x.append(max)
    print (x)
    print ()
        
    with open ('prvalues.txt', 'a') as f:
        for x in data:
            f.write (id + str(x[0]) + str(x[1]))
        
    return sumP/k
