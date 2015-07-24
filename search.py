import sys, string, operator, re, math
from bs4 import BeautifulSoup

# python search/search.py search-text

def xml(arg):
    # takes only the text inside of a p tag
    # of a xml file and returns it as a string
    soup = BeautifulSoup(open(arg), 'lxml')
    final=''
    text = soup.find_all('p')
    for words in text:
        final+=words.get_text()
    print (final)
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
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


def idf(tf, n, N):
    # tf = term frequency
    # n = num docs with term
    # N = num docs total
    w = tf*math.log((n/N), 2)
    return w

def length(w, l, A):
    # current weight
    # l = length of current doc
    # A = average length of docs
    w /= (l/A)
    return w

def main(argv):
    files = readfiles(argv[1])

    # parses the text (takes the text inside the p tags)
    text = []
    for theFile in files:
        text.append(formatText(xml(theFile)).split(' '))
    #print (text)
    
    # goes through each word in each of the documents
    # and adds it to a term dictionary
    terms = {}
    for x in range(len(text)):
        for y in text[x]:
            docNo = str(x+1)
            if y in terms:
                if docNo in terms[y]:
                    terms[y][docNo]+=1
                else:
                    terms[y][docNo]=1
            else:
                terms[y] = {docNo: 1}
    print (terms)
    
    # weighing options
    options = input ('enter 1 - idf, 2 - length normalization: ')
    if '1' in options:
        N = len(text)
        for x in terms:
            n = len(terms[x])
            print (terms[x])
            for y in terms[x]:
                terms[x][y] = idf(terms[x][y], n, N)
    if '2' in options:
        avg = 0
        lengths = []
        for x in text:
            avg+=len(x)
            lengths.append(len(x))
        avg /= len(text)
        for x in terms:
            terms[x] = length(terms[x], avg, length[int(x)])

    print (terms)
    # user input
    query = input('Search: ')
    keyWords = formatText(query).split(' ')
    
    # goes through each word in the query
    # and adds up the occurences of the words from each document
    foundDocs = {}
    for word in keyWords:
        for doc in terms[word]:
            if doc in foundDocs:
                foundDocs[doc]+=terms[word][doc]
            else:
                foundDocs[doc]=terms[word][doc]

    
    # prints the sorted (in reverse) dictionary
    foundDocs = sorted(foundDocs.items(), key=operator.itemgetter(1), reverse=True)
    print (foundDocs)



if __name__=="__main__":
    main(sys.argv)
