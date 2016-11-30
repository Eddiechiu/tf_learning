from bs4 import BeautifulSoup
import re
import urllib2
from collections import OrderedDict
import nltk

class Papers():
    def __init__(self, title, abstract):
        self.title = title
        self.abstract = abstract
        wordCount_dict = {}
        wordCount_list = []
        content = title + abstract
        wordSplit = content.split(' ')
        for word in wordSplit:
            # take the stem of each word
            word = nltk.stem.snowball.EnglishStemmer().stem(word)
            if word in invalid_words:
                continue

            if word in wordCount_dict:
                wordCount_dict[word] += 1
            else:
                wordCount_dict[word] = 1

        for item in wordCount_dict.items():
            wordCount_list.append(item)

        self.wordCount = sorted(wordCount_list, key=lambda word: word[1], reverse=1)


def content_grab(pageNum, pattern):
    url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?...' \
          'punumber=77&filter%3DAND%28p_IS_Number%3A7368234%29&pageNumber=' + str(pageNum)
    headers = {'User-Agent': 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
    req = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(req)
    data = response.read()
    data = data.decode('GBK')
    return pattern.findall(data)

pattern_title = re.compile(r'<span id="art-abs-title-\d{7}">(.*?)</span>')

# \s is used to match the content that have some void char(such as blankspace, \n, tab). There are lots of such void chars in html.
pattern_abstract = re.compile(r'<p>[\s]*(.*?)[\s]*<a href="/document')

# in which each element is the title of the paper
paper_titles = []
# in which each element is the abstract of the paper
paper_abstracts = []
# the list consists of the objects that contain the paper's title and its abstract  
papers = []
# all words appear in the papers
words = set()

wordSplit = []

# such as wordCount_dict = {'the': 11, 'a': 23, ... }
wordCount_dict = {}
wordCount_list = []
invalid_words = set(['of', 'and', 'for', 'in', 'magnet', 'the', 'a', 'on', 'by', 'with', '<img', '<inline-formula>', 'use', '</inline-formula>',
'analysi', 'studi', 'to', 'at', '}">', 'from', 'an', 'via', 'after', 'before'])

for num in range(1,15):  # there are 14 pages
    print('page ' + str(num) + ' start, wait...')

    for title in content_grab(pageNum=num, pattern=pattern_title):
      paper_titles.append(title)

    for abstract in content_grab(pageNum=num, pattern=pattern_abstract):
      paper_abstracts.append(abstract)

    # combine_til_abs = zip(paper_titles, paper_abstracts)
    # papers = dict((title, abstract) for title, abstract in combine_til_abs)
    for i in range(len(paper_titles)):
        papers.append(Papers(paper_titles[i], paper_abstracts[i]))

    del paper_titles[:]
    del paper_abstracts[:]

    print('page ' + str(num) + ' finished.')

for paper in papers:
    wordSplit = paper.title.split(' ')
    for word in wordSplit:
        # take the stem of each word
        word = nltk.stem.snowball.EnglishStemmer().stem(word)
        if word in invalid_words:
            continue

        if word in wordCount_dict:
            wordCount_dict[word] += 1
        else:
            wordCount_dict[word] = 1

#   words = words.union(set(wordSplit))

for item in wordCount_dict.items():
    wordCount_list.append(item)

wordCount_list = sorted(wordCount_list, key=lambda word: word[1], reverse=1)

# word_number = 1
# for i in wordCount_list:
#     print str(word_number) + i[0] + ': ' + str(i[1])
#     word_number += 1 

word_number = 1
for paper in papers:
    print paper.wordCount