import sys
import string, operator, re
from bs4 import BeautifulSoup


def xml(arg):
    soup = BeautifulSoup(open(arg), 'lxml')
    final=''
    text = soup.find_all('p')
    text = text[0:10]
    for words in text:
        final+= words.get_text()
    return final


def readfiles(f):
    files = []
    with open (f, 'r') as fp:
        for line in fp:
            files.append(line[0:len(line)-1])
    return files


def formatText(text):
    # formats the user input:
    # - makes it all lowercase
    # - replaces punctuation with spaces
    text =text.lower()
    exclude = set(string.punctuation)
    exclude2 = set(str(b) for b in range(0, 10))
    text = ''.join(ch for ch in text if ch not in exclude and ch not in exclude2)
    text = re.sub( '\s+', ' ', text).strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def main(argv):
    files = readfiles(argv[1])
    docs = []
    for theFile in files:
        docs.append(xml(theFile))
        
    text = []
    for x in docs:
        text.append(formatText(x))
        
    terms = {}
    for x in range(len(text)):
        for y in text[x].split(' '):
            docNo = str(x+1)
            if y in terms:
                if docNo in terms[y]:
                    terms[y][docNo]+=1
                else:
                    terms[y][docNo]=1
            else:
                terms[y] = {docNo: 1}

    print (terms)

    query = input('Search: ')
    keyWords = formatText(query).split(' ')

    foundDocs = {}
    for word in keyWords:
        for doc in terms[word]:
            if doc in foundDocs:
                foundDocs[doc]+=terms[word][doc]
            else:
                foundDocs[doc]=terms[word][doc]
    foundDocs = sorted(foundDocs.items(), key=operator.itemgetter(1), reverse=True)
    print (foundDocs)



if __name__=="__main__":
    main(sys.argv)
