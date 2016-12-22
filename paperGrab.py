import re
import urllib
from collections import OrderedDict, Counter
import nltk
import pdb
from functools import reduce
import pandas as pd

class Paper():
    def __init__(self, title, abstract):
        self.title = title
        self.abstract = abstract

        content = title + abstract
        wordSplit = content.split(' ')
        wordSplit = [nltk.stem.snowball.EnglishStemmer().stem(word).strip(' .()[]:,') for word in wordSplit]

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

# such as wordCount_dict = {'magnet': 11, 'YBCO': 23, ... }
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

##### 0. Start of the main process
##### 1. Download the title and abstract content and transform them into Paper class
for num in range(1,2):  # there are 14 pages
    print('page ' + str(num) + ' start, wait...')

    paper_titles = [title for title in content_grab(pageNum=num, pattern=pattern_title)]
    paper_abstracts = [abstract for abstract in content_grab(pageNum=num, pattern=pattern_abstract)]
    papers = [Paper(paper_titles[i], paper_abstracts[i]) for i in range(len(paper_titles))]

    print('page ' + str(num) + ' finished.')

# store the word count in a list in which each element is saved as dataFrame 
wordCount_dataFrame_list = [pd.DataFrame(list(dict(paper.wordCount).items()), columns=['Word', 'Count']) for paper in papers]
pdb.set_trace()
print(wordCount_dataFrame_list)