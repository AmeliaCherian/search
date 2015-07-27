import sys
from search import main

def main2 (argv):
    files = argv[1:2]
    topic = argv[2]
    topics = {}
    with open (topic, 'r') as f:
        for lines in f:
            info = lines.split(' ')
            topics[info[0]] = info[2]
    print (topics)
        
    qrel = {}
    for x in files:
        with open (x, 'r') as f:
            for lines in f:
                info = lines.split(' ')
                torf = (info[3]).replace('\n', '')
                if torf == '1':
                    if info[0] in qrel:
                        qrel[info[0]][info[2]] = 1 
                    else:
                        qrel[info[0]] = {info[2]:1}
    for q in topics:
        ret = main(topics[q], sys.argv[3:])
        rev = qrel[q]
    
    for x in rev:
        if x in qrels:
            cP+=1
            qrels.pop(x)
        else:
            fP+=1
    fN+=len(qrels)
    print (cP, fP, fN)
    
if __name__ == '__main__':
    main2(sys.argv)
