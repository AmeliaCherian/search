import sys, string, operator, re, math
from itertools import islice
from bs4 import BeautifulSoup
from eval import evaluate

#python search.py topics/301-350.T qrels/301-350.cd45.LA docs/*

def xml(arg, d):
    # takes only the text inside of a p tag
    # of a xml file and returns it as a string
    
    soup = BeautifulSoup(open(arg), 'lxml')
    final=d
    these = soup.find_all('doc')
    
    for docs in these:
        the = ''
        docno = docs.find('docno')
        text = docs.find_all('p')
        
        for words in text:
            the += formatText(words.get_text())
        final[docno.get_text().strip()] = the.split(' ')
    
    return final

def readfiles(f):
    # takes a file that contains names of files
    # and returns a list of those files
    
    files = []
    with open (f, 'r') as fp:
        for line in fp:
            files.append(line[0:len(line)-1])
    
    return files


def formatText(text):
    # formats the user input:
    #  - makes it all lowercase
    #  - replaces punctuation and numbers with spaces
    #  - removes multiple spaces
    
    text = text.lower()
    text.replace('-', ' ')
    exclude = set(string.punctuation)
    exclude2 = set(str(b) for b in range(0, 10))
    text = ''.join(ch for ch in text if ch not in exclude and ch not in exclude2)
    text = re.sub( '\s+', ' ', text).strip()
    text = ' '.join(text.split())
    text.strip()
    
    return text


def idf(tf, n, N):
    # tf = term frequency
    # n = num docs with term
    # N = num docs total
    
    w = -1*tf*math.log((n/N), 2)
    
    return w

def length(tf, l, A):
    # tf = current weight
    # l = length of current doc
    # A = average length of docs
    
    w = tf/((l/A)**(1/2))
    #put sq rt to lower length's effect on weight

    return w

def findTerms(files):
    #files = readfiles(files[1])

    # parses the text (takes the text inside the p tags)
    text = {}
    for theFile in files:
        text = (xml(theFile, text))
        
    # goes through each word in each of the documents
    # and adds it to a term dictionary
    terms = {}
    for docNo in text:
        for y in text[docNo]:
            if y in terms:
                if docNo in terms[y]:
                    terms[y][docNo]+=1
                else:
                    terms[y][docNo]=1
            else:
                terms[y] = {docNo: 1}
    
    # weighing options
    options = input ('enter: \t1 - idf,\n\t2 - length normalization: ')
    if '1' in options:
        N = len(text)
        for x in terms:
            n = len(terms[x])
            for y in terms[x]:
                terms[x][y] = idf(terms[x][y], n, N)

    if '2' in options:
        avg = 0
        lengths = [len(x) for x in text]
        avg = float(sum(lengths))/len(lengths)
        
        for x in terms:
            for y in terms[x]:
                terms[x][y] = length(terms[x][y], len(text[y]), avg)
    return terms
    #print (list(islice(terms.items(), 5)))


def qrels(files):
    # files is a list of files
    qrel = {}
    for x in files:
        with open (x, 'r') as f:
            for lines in f:
                info = lines.split(' ')
                torf = (info[3]).replace('\n', '')
                if info[0] in qrel:
                    qrel[info[0]][info[2]]=torf
                else:
                    qrel[info[0]] = {info[2]:torf}
    return (qrel)
    
def ranks (q, terms):    
    
    # user input
    query = q
    keyWords = formatText(query).split(' ')
    
    # goes through each word in the query
    # and adds up the occurences of the words from each document
    foundDocs ={}
    for word in keyWords:
        if word in terms:
            for doc in terms[word]:
                if doc in foundDocs:
                    foundDocs[doc]+=terms[word][doc]
                else:
                    foundDocs[doc]=terms[word][doc]

    
    # prints the sorted (in reverse) dictionary
    #foundDocs = sorted(foundDocs.items(), key=operator.itemgetter(1), reverse=True)
    return foundDocs

def main(files):
    topic = files[1]
    topics = {}
    with open (topic, 'r') as f:
        for lines in f:
            info = lines.split(' ')
            topics[info[0]] = info[1]
    
    terms = findTerms(sys.argv[3:])
    qrel = qrels([files[2]])

    for q in topics:
        ret = ranks(topics[q], terms)
        ret = list(ret.keys())
 
        rel = qrel[q]

        print (q, topics[q])
        print (ret)
        print (rel)
        print (evaluate(ret, rel))
        print ('\n')

        
if __name__=="__main__":
    #q = input('Search: ')
    print (main(sys.argv))
