import sys


def main (argv, rankList):
    files = argv[1:]

    qrel = {}
    for x in files:
        with open (x, 'r') as f:
            for lines in f:
                info = lines.split(' ')
                if info[0] in qrel:
                    qrel[info[0]][info[2]] = (info[3]).replace('\n', '')
                else:
                    qrel[info[0]] = {info[2]:info[3].replace('\n','')}
    print (qrel)
    
    numC = len(qrels)
    for x in rankList:
        if x in qrels:
            cP+=1
            qrels.pop(x)
        else:
            fP+=1
    fN+=len(qrels)
    print (cP, fP, fN)
    
if __name__ == '__main__':
    main(sys.argv, [0,0])
