import sys, string, operator, re
from bs4 import BeautifulSoup

# python search/search.py search-text

def xml(arg):
    # takes only the text inside of a p tag
    # of a xml file and returns it as a string
    soup = BeautifulSoup(open(arg), 'lxml')
    final=''
    text = soup.find_all('p')#[:]
    for words in text:
        final+= words.get_text()
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

def main(argv):
    files = readfiles(argv[1])

    # parses the text (takes the text inside the p tags)
    text = []
    for theFile in files:
        text.append(formatText(xml(theFile)).split(' '))
    print (text)
    
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
