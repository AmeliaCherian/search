import sys, string, operator, re, math
from itertools import islice
from collections import defaultdict
from bs4 import BeautifulSoup
from evaluate import evaluate
from porterstemmer import toStem


def xml(parserOption, files, d):
    # takes only the text inside of a p tag
    # of a xml file and returns it as a string

    soup = BeautifulSoup(open(files), 'lxml')
    final=d

    these = soup.find_all('doc')
    
    for docs in these:
        # DOC
        the = ''
        docno = docs.find('docno')
        if parserOption == '1':
            the += formatText(str(docs))

        # DOC w/o tags
        if parserOption == '2':
           the += formatText(docs.get_text())

        # TEXT  
        if parserOption == '3':
            text2 = docs.find_all('text')
            for words in text2:
                the += formatText(str(text2))

        # TEXT w/o tags
        if parserOption == '4':
            text = docs.find_all('text')
            for words in text:
                the += formatText(words.get_text())

        
        final[docno.get_text().strip()] = the.split(' ')

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


# ORIGINAL WEIGHT IS IN search/ser.txt
def weight(options, tf, n, N, l, A):
    # tf = term frequency
    # n = num docs with term
    # N = num docs total

    w = tf
    listing = [tf]
    
    if '1' in options:
        w = w *math.log((N/n), 2)
        listing.append(w)
    
    # l = length of current doc
    # A = average length of docs
    if '2' in options:
        w = w/((l/A)**(1/2))
        listing.append(w)
       
    return listing





def findTerms(files):
    #files = readfiles(files[3])

    stop = ["a", "an", "and", "are", "as", "at", "be", "but", "by",
            "could", "do", "did", "for", "if", "in", "into", "is",
            "it", "for", "had", "has", "no", "not", "of",
            "on", "or", "such", "that", "the", "them", "their", "then", "there",
            "these", "they", "this", "to", "was", "will", "with"]
    
    # parses the text
    text = {}
    options = input('1 - DOC, 2 - DOC no tags, 3 - TEXT, 4 - TEXT no tags: ')
    
    for theFile in files:
        text = (xml(options, theFile, text))
     
    # goes through each word in each of the documents
    # and adds it to a term dictionary
    terms = defaultdict(lambda: defaultdict(lambda:0))
    for docNo in text:
        for y in text[docNo]:
            if y not in stop:
                terms[y][docNo]+=1

    l = {x:len(text[x]) for x in text}
    
    return [terms, l]




def ranks (q, terms):    
    
    # user input
    keyWords = formatText(q).split(' ')
    
    foundDocs =defaultdict(lambda:0)
    for word in keyWords:
        if word in terms:
            print (word)
            print (terms[word])
            print()
            for doc in terms[word]:
            	foundDocs[doc]+=terms[word][doc]
    
    return foundDocs




def main(files):
    #clears files
    with open ('prvalues.txt', 'w'): pass
    with open ('ranks.txt', 'w'):  pass

    #goes through the topics file and makes a dict
    topic = files[1]
    topics = {}
    with open (topic, 'r') as f:
        for lines in f:
            info = lines.split(' ')
            topics[info[0]] = ' '.join(info[1:])

    # goes through a qrels file
    # makes a dict {query: list of rel docs}
    qrel = qrels([files[2]])


    # goes through the text of all the docs
    # makes a term dict, also lengths of docs
    found = findTerms(files)
    terms = found[0]
    l = found [1]

    
    binOptions = input('1 - binary, 2 - not?')
    
    if binOptions != '1':
        wOptions = input ('enter: \t1 - idf,\n\t2 - length normalization: ')
        N = len(l)

        avg = float(sum(l.values()))/len(l)

        for x in terms:
            n = len(terms[x])
            for y in terms[x]:
            	thing = weight(wOptions, terms[x][y], n, N, l[y], avg)
            	terms[x][y] = thing[-1]


    for q in topics:
        rank = ranks(topics[q], terms)
        some = sorted(rank.items(), key = operator.itemgetter(1), reverse=True)
        ret = list(rank.keys())
        
        count = 0
        output = ''
        for doc in some:
            count+=1
            output += (q+' Q0 '+doc[0]+' '+str(count)+' '+str(doc[1])+' x\n')

        with open ('ranks.txt', 'w') as f:
            f.write(output)
            
        rel = qrel[q]

        print (q, topics[q])
        print (evaluate(q, ret, rel))
        print ('\n')

        
if __name__=="__main__":
    #q = input('Search: ')
    main(sys.argv)

    
    

