import re
import urllib
from collections import OrderedDict, Counter
import nltk
import pdb
from functools import reduce
import pandas as pd
from functools import reduce
import time

# Paper Class that contains title, abstract and valid word count of each paper
class Paper():
    def __init__(self, title, abstract):
        self.title = title
        self.abstract = abstract

        content = title + abstract
        wordSplit = content.split(' ')
        wordSplit = [nltk.stem.snowball.EnglishStemmer().stem(word).strip(' .()[]:,') for word in wordSplit]

        words = [word for word in wordSplit if word not in invalid_words]
        wordCount = dict(Counter(words))
        keys = [item[0] for item in wordCount.items()]
        values = [item[1] for item in wordCount.items()]
        self.wordCount = pd.DataFrame(data=values, index=keys, columns=['count'])

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

invalid_words = set([
    'this', 'that', 'these', 'those', 'the', 'have', 'has', 'as', 'it',
    'in', 'on', 'of', 'for', 'by', 'with', 'to', 'at', 'from', 'after', 'before', 'via', 'such', 'and', 'near', 'between',
    'when', 'where', 'who', 'what', 'which', 'how', 'am', 'is', 'are', 'was', 'were', 'not', 'a', 'an', 'not', 'should', 'could',
    'we', 'our', 'they', 'their',
    'because', 'so', 'therefore',
    'first', 'second',
    'use', 'have',
    '</inline-formula>', '}">', '<inline-formula>', '<img',
    'paper', 'test',
    'one', 'two', 'three', 'four', 'five', 'six', 'be'
     ])

##### 0. Start of the main process
##### 1. Download the title and abstract content and transform them into Paper class
# the list contains all the papers information, in which each element is Paper object
papers = []
tag1 = time.clock()
for num in range(1,15):  # there are 14 pages
    print('page ' + str(num) + ' start, wait...')

    paper_titles = [title for title in content_grab(pageNum=num, pattern=pattern_title)]
    paper_abstracts = [abstract for abstract in content_grab(pageNum=num, pattern=pattern_abstract)]
    papers = papers + [Paper(paper_titles[i], paper_abstracts[i]) for i in range(len(paper_titles))]

    print('page ' + str(num) + ' finished.')
tag2 = time.clock()
print('%.03f seconds for Step_1: Data downloading and reorgnization' % (tag2-tag1))

##### 2. count all the words in papers using reduce

# very important!! if using reduce to simplify the counting process, the function pd.DataFrame.add should be redefined by pass 0 to fill_value of the function, like this:
def sum_data(x, y):
    return pd.DataFrame.add(x, y, fill_value=0)

tag1 = time.clock()
all_wordCount = reduce(sum_data, [paper.wordCount for paper in papers])
tag2 = time.clock()
print('%.03f seconds for Step_2: Merge all wordCount into one DataFrame' % (tag2-tag1))

print(all_wordCount.sort_values(by='count', ascending=False))
pdb.set_trace()


# next step:
# 0. how to get the whole abstract, rather than part of it
# 1. multiprocesses
# 2. pretty plot