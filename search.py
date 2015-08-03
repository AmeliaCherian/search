import sys, string, operator, re, math
from itertools import islice
from collections import defaultdict
from bs4 import BeautifulSoup
from evaluate import evaluate

#python search.py topics/301-350.T qrels/301-350.cd45.LA docs/*

def xml(options, arg, d):
    # takes only the text inside of a p tag
    # of a xml file and returns it as a string

    soup = BeautifulSoup(open(arg), 'lxml')
    final=d

    these = soup.find_all('doc')
    
    for docs in these:
        the = ''
        docno = docs.find('docno')
        if options == '1':
            the += formatText(str(docs))
            final[docno.get_text().strip()] = the.split(' ')

        if options == '2':
           the += formatText(docs.get_text())
           final[docno.get_text().strip()] = the.split(' ')

        if options == '3':
            text2 = docs.find_all('text')
            for words in text2:
                the += formatText(str(text2))
                final[docno.get_text().strip()] = the.split(' ')

        if options == '4':
            text = docs.find_all('text')
            for words in text:
                the += formatText(words.get_text())
                final[docno.get_text().strip()] = the.split(' ')
    print (the)
    print(final) 
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
    #exclude2 = set(str(b) for b in range(0, 10))
    text = ''.join(ch for ch in text if ch not in exclude) #and ch not in exclude2)
    text = re.sub( '\s+', ' ', text).strip()
    text = ' '.join(text.split())
    text.strip()
    
    return text


def weight(options, tf, n, N, l, A):
    # tf = term frequency
    # n = num docs with term
    # N = num docs total

    w = tf
    
    if '1' in options:
       w = w *math.log((N/n), 2)

    # l = length of current doc
    # A = average length of docs
    if '2' in options:
        w = w/((l/A)**(1/2))
       
    return w

def findTerms(files):
    #files = readfiles(files[3])

    # parses the text (takes the text inside the p tags)
    text = {}
    options = input("1 - DOC, 2 - DOC no tags, 3 - TEXT, 4 - TEXT no tags: ")
    
    for theFile in files:
        text = (xml(options, theFile, text))
        
    # goes through each word in each of the documents
    # and adds it to a term dictionary
    terms = defaultdict(lambda: defaultdict(lambda:0))
    for docNo in text:
        for y in text[docNo]:
            terms[y][docNo]+=1
    
    # weighing options
    options = input ('enter: \t1 - idf,\n\t2 - length normalization: ')
    N = len(text)
    
    lengths = [len(x) for x in text]
    avg = float(sum(lengths))/len(lengths)
        
    for x in terms:
        n = len(terms[x])
        for y in terms[x]:
            terms[x][y] = weight(options, terms[x][y], n, N, len(text[y]), avg)

                
    return terms
    #print (list(islice(terms.items(), 5)))


def qrels(files):
    # files is a list of files
    qrel = defaultdict(lambda: defaultdict(lambda: 0))
    for x in files:
         with open (x, 'r') as f:
            for lines in f:
                info = lines.split(' ')
                torf = (info[3]).replace('\n', '')
                qrel[info[0]][info[2]]=torf

    return (qrel)
    
def ranks (q, terms):    
    
    # user input
    query = q
    keyWords = formatText(query).split(' ')

    options = ("bin or not?")
    # goes through each word in the query
    # and adds up the occurences of the words from each document
    foundDocs =defaultdict(lambda:0)
    for word in keyWords:
        if word in terms:
            for doc in terms[word]:
                if options ==1:
                    foundDocs[doc]==1
                else:
                    foundDocs[doc]+=terms[word][doc]
    
    # prints the sorted (in reverse) dictionary
    foundDocs = dict(sorted(foundDocs.items(), key=operator.itemgetter(1), reverse=True))
    return foundDocs

def main(files):
    
    # clears files
    with open ("prvalues.txt", "w"): pass
    with open ("ranks.txt", "w"):  pass


    topic = files[1]
    topics = {}
    with open (topic, 'r') as f:
        for lines in f:
            info = lines.split(' ')
            topics[info[0]] = ' '.join(info[1:])
    
    terms = findTerms(sys.argv[3:])
    qrel = qrels([files[2]])

    for q in topics:
        rank = ranks(topics[q], terms)
        some = sorted(rank.items(), key = operator.itemgetter(1), reverse=True)
        ret = list(rank.keys())
        count = 0
        for doc in some:
            with open ('ranks.txt', 'a') as f:
                count+=1
                f.write(q+' Q0 '+doc[0]+' '+str(count)+' '+str(doc[1])+' x\n')
   
        rel = qrel[q]

        print (q, topics[q])
        print (evaluate(q, ret, rel))
        print ('\n')

        
if __name__=="__main__":
    #q = input('Search: ')
    main(sys.argv)
