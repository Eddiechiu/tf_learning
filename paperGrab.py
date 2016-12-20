import re
import urllib
from collections import OrderedDict
import nltk
from collections import Counter
import pdb

class Paper():
    def __init__(self, title, abstract):
        self.title = title
        self.abstract = abstract
        # wordCount_dict = {}
        # wordCount_list = []
        content = title + abstract
        wordSplit = content.split(' ')
        wordSplit = [nltk.stem.snowball.EnglishStemmer().stem(word).strip(' .()[]:,') for word in wordSplit]

        # # conventional way to pick up the valid word, get its stemmer and count all words
        # for word in wordSplit:
        #     # take the stem of each word
        #     word = nltk.stem.snowball.EnglishStemmer().stem(word).strip(' .()[]:,')
        #     if word in invalid_words:
        #         continue
        #     if word in wordCount_dict:
        #         wordCount_dict[word] += 1
        #     else:
        #         wordCount_dict[word] = 1

        # for item in wordCount_dict.items():
        #     wordCount_list.append(item)

        # self.wordCount = sorted(wordCount_list, key=lambda word: word[1], reverse=1)
        words = [word for word in wordSplit if word not in invalid_words]
        self.wordCount = Counter(words)

def content_grab(pageNum, pattern):
    url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?...' \
          'punumber=77&filter%3DAND%28p_IS_Number%3A7368234%29&pageNumber=' + str(pageNum)
    headers = {'User-Agent': 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}
    data = urllib.request.urlopen(url).read()
    data = data.decode('GBK')
    return pattern.findall(data)

# patterns of matching titles and abstracts
pattern_title = re.compile(r'<span id="art-abs-title-\d{7}">(.*?)</span>')
# \s is used to match the content that have some void char(such as blankspace, \n, tab). There are lots of such void chars in html.
pattern_abstract = re.compile(r'<p>[\s]*(.*?)[\s]*<a href="/document')

# all words appear in the papers
words = set()

wordSplit = []

# such as wordCount_dict = {'the': 11, 'a': 23, ... }
wordCount_dict = {}
wordCount_list = []

invalid_words = set([
    'this', 'that', 'these', 'those', 'the', 'have', 'has', 'as',
    'in', 'on', 'of', 'for', 'by', 'with', 'to', 'at', 'from', 'after', 'before', 'via', 'such', 'and', 'near', 'between',
    'when', 'where', 'who', 'what', 'which', 'how', 'am', 'is', 'are', 'was', 'were', 'not', 'a', 'an', 'not', 'should', 'could',
    'we', 'our', 'they', 'their',
    'because', 'so', 'therefore',
    'first', 'second',
    'use', 'have',
    '</inline-formula>', '}">', '<inline-formula>', '<img',
    'paper', 'test',
     ])

#####----  start of the main process  ----####
# download the title and abstract content and transform them into Paper class
for num in range(1,2):  # there are 14 pages
    print('page ' + str(num) + ' start, wait...')

    paper_titles = [title for title in content_grab(pageNum=num, pattern=pattern_title)]
    paper_abstracts = [abstract for abstract in content_grab(pageNum=num, pattern=pattern_abstract)]

    # combine_til_abs = zip(paper_titles, paper_abstracts)
    # papers = dict((title, abstract) for title, abstract in combine_til_abs)
    papers = [Paper(paper_titles[i], paper_abstracts[i]) for i in range(len(paper_titles))]

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

for paper in papers:
    print(paper.wordCount)
    print('\n')