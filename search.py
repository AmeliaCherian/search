import sys, string, operator, re, math
from itertools import islice
from collections import defaultdict
from bs4 import BeautifulSoup
from evaluate import evaluate
from porterstemmer import toStem

# python search.py topics/ten.T qrels/ten.LA docs/*


def xml(parserOption, files, final):
    # takes only the text inside of a p tag
    # of a xml file and returns it as a string

    p = BeautifulSoup(open(files), 'lxml')
    docList = p.find_all('doc')
    
    for doc in docList:
        # DOC
        included = ''
        docno = doc.find('docno')
        if '1' in parserOption:
            included += formatText(str(doc))

        # DOC w/o tags
        elif '2' in parserOption:
           included += formatText(doc.get_text())

        # TEXT  
        elif '3' in parserOption:
            text = doc.find_all('text')
            for words in text:
                included += formatText(str(text))

        # TEXT w/o tags
        elif '4' in parserOption:
            text = doc.find_all('text')
            for words in text:
                included += formatText(words.get_text())
        
        if included!='':
            final[docno.get_text().strip()] = included.split(' ')

    return final


def formatText(text):
    # formats the user input:
    #  - makes it all lowercase
    #  - replaces punctuation and numbers with spaces
    #  - removes multiple spaces
    
    text = text.lower()
    text = text.replace('-', ' ')

    exclude = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)

    text = toStem([text])
    text = re.sub( '\s+', ' ', text).strip()

    text = ' '.join(text.split())
    text.strip()
    
    return text


def findQrels(files):
    
    # files is a list of files
    qrel = defaultdict(lambda: defaultdict(lambda: 0))
    for x in files:
        with open (x, 'r') as f:
            for lines in f:
                info = lines.split(' ')
                torf = (info[3]).replace('\n', '')
                qrel[info[0]][info[2]] = torf

    return qrel


def weight(options, tf, n, N, l, A):
    
    # tf = term frequency
    # n = num docs with term
    # N = num docs total

    w = tf
    listing = [tf]

    # idf
    if '1' in options:
        w = w*math.log((N/n), 2)
        listing.append(w)
    
    # l = length of current doc
    # A = average length of docs

    # length normalization
    if '2' in options:
        w = w/((l/A)**(1/2))
        listing.append(w)
       
    return listing


def findTerms(files):
    
    stop = ["a", "an", "and", "are", "as", "at", "be", "but", "by",
            "could", "do", "did", "for", "if", "in", "into", "is",
            "it", "for", "had", "has", "no", "not", "of",
            "on", "or", "such", "that", "the", "them",
            "their", "then", "there", "these", "they",
            "this", "to", "was", "will", "with"]
    
    # parses the text
    text = {}
    options = input('1 - DOC, 2 - DOC no tags, 3 - TEXT, 4 - TEXT no tags: ')
    
    for f in files:
        text = (xml(options, f, text))
     
    # goes through each word in each of the documents
    # and adds it to a term dictionary
    terms = defaultdict(lambda: defaultdict(lambda:0))

    for docNo in text:
        for y in text[docNo]:
            if y not in stop:
                terms[y][docNo]+=1

    l = {x:len(text[x]) for x in text}
    
    return [terms, l]


def getRanks (q, terms):    

    keyWords = formatText(q).split(' ')
    
    foundDocs =defaultdict(lambda:0)
    for word in keyWords:
        if word in terms:
            #print (word)
            #print (terms[word])
            for doc in terms[word]:
            	foundDocs[doc]+=terms[word][doc]
    
    return foundDocs


def main(files):
    
    #clears files
    with open ('prvalues.txt', 'w'): pass
    with open ('ranks.txt', 'w'):  pass

    #goes through the topics file and makes a dict
    topics = {}
    with open (files[1], 'r') as f:
        for lines in f:
            info = lines.split(' ')
            topics[info[0]] = ' '.join(info[1:])

    # goes through a qrels file
    # makes a dict {query: list of rel docs}
    qrel = findQrels([files[2]])


    # goes through the text of all the docs
    # makes a term dict, also lengths of docs
    found = findTerms(files)
    terms = found[0]
    l = found [1]
    N = len(l)
    
    binOptions = input('1 - binary, 2 - not? ')
    
    if binOptions != '1':
        wOptions = input ('enter: 1 - idf, 2 - length normalization: ')
        
        avg = float(sum(l.values()))/len(l)

        for x in terms:
            n = len(terms[x])
            for y in terms[x]:
            	thing = weight(wOptions, terms[x][y], n, N, l[y], avg)
            	terms[x][y] = thing[-1]

    else:
        terms = {y:{x:1 for x in terms[y] if x!=0} for y in terms}
        
    output = ''
    ap = []
    
    for q in topics:
        #q is the topic number
        rank = getRanks(topics[q], terms)
        sortRank = sorted(rank.items(), key = operator.itemgetter(1), reverse=True)
        ret = list(x[0] for x in sortRank)
        
        # for the export
        count = 0
        for doc in sortRank:
            count+=1
            output += (q+' Q0 '+doc[0]+' '+str(count)+' '+str(doc[1])+' x\n')

        rel = qrel[q]

        print (q, topics[q].replace('\n', ''))
        ap.append(evaluate(q, ret, rel, N))
        print (ap)
        print ('\n')
        
    maps  = sum(ap)/len(ap)
    print (maps)
    # exports precision and recall values
    with open ('ranks.txt', 'w') as f:
            f.write(output)


if __name__=="__main__":
    main(sys.argv)

    
    

