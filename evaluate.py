import sys
#from search import main, findTerms

def evaluate (id, rlist, qrel, numDocs):
    ret = len(rlist)
    k = min(10, ret)

    # goes through the qrel and makes a list of relevant docs
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
    
    for point in range(k):
        if rlist[point] in relList:
            retrel+=1
        else:
            fP +=1
                
        fN = len(list(x for x in relList if x not in rlist))
        tN = numDocs - rel - fP

        fPRate = (fP/(fP+tN))
        specificity =  (tN/(fP+tN))
        ap = (1/rel)
        
        precision = retrel/(point+1)
        sumP += precision
        recall = retrel/rel
        
        data.append([recall, precision])

        print ((point+1), data[point])


    for some in range(0, 11):
        n = some/10
        mx = 0
        for l in data:
            if l[0]==n:
                mx = l[1]
                break
            elif l[0]>n and l[1]>mx:
                mx = l[1]
        x.append(mx)
    print (x)
        
    with open ('iprec.txt', 'a') as f:
        for some in range(0, 11):
            f.write (id +' '+ str(some/10)+' '+ str(x[some])+'\n')
        
    return sumP/k
