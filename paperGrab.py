import re
import urllib
import nltk
import pdb
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from multiprocessing import Pool
from collections import Counter

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

# get papers' content (title, abstract and word count, stored in Paper class) from page pageNum 
def get_papers(pageNum):
    start = time.clock()
    print('page ' + str(pageNum) + ' start, wait...')
    paper_titles = [title for title in content_grab(pageNum=pageNum, pattern=pattern_title)]
    paper_abstracts = [abstract for abstract in content_grab(pageNum=pageNum, pattern=pattern_abstract)]
    papers = [Paper(paper_titles[i], paper_abstracts[i]) for i in range(len(paper_titles))]
    end = time.clock()
    print('page ' + str(pageNum) + ' finished, %0.2f seconds used.' % (end-start))
    return papers

# very important!! if using reduce to simplify the counting process, the function pd.DataFrame.add should be redefined by pass 0 to fill_value of the function, like this:
def data_Frame_sum(x, y):
    return pd.DataFrame.add(x, y, fill_value=0)

def topWords_plot(all_wordCount, top):
    result = all_wordCount.sort_values(by='count', ascending=False)[:top]
    words = tuple(result.index)
    fre = tuple(result.values.flatten())
    y_pos = np.arange(len(words))   

    plt.barh(y_pos, fre, align='center', alpha=0.4)
    plt.yticks(y_pos, words)
    plt.xlabel('Frequencies')
    plt.title('Wrod Frequencies in Papers')
    plt.show()

# patterns of matching titles and abstracts
pattern_title = re.compile(r'<span id="art-abs-title-\d{7}">(.*?)</span>')
# \s is used to match the content that have some void char(such as blankspace, \n, tab). There are lots of such void chars in html.
pattern_abstract = re.compile(r'<p>[\s]*(.*?)[\s]*<a href="/document')

invalid_words = set([
    'this', 'that', 'these', 'those', 'the', 'have', 'has', 'as', 'it',
    'in', 'on', 'of', 'for', 'by', 'with', 'to', 'at', 'from', 'after', 'before', 'via', 'such', 'and', 'near', 'between',
    'when', 'where', 'who', 'what', 'which', 'how', 'am', 'is', 'are', 'was', 'were', 'not', 'a', 'an', 'not', 'should', 'could', 'been',
    'we', 'our', 'they', 'their',
    'because', 'so', 'therefore',
    'first', 'second',
    'use', 'have',
    '</inline-formula>', '}">', '<inline-formula>', '<img',
    'paper', 'test',
    'one', 'two', 'three', 'four', 'five', 'six', 'be',
    'system', 'investig', 'develop', 'design',
     ])

##### 0. Start of the main process
##### 1. Download the title and abstract content and transform them into Paper class
# the list contains all the papers information, in which each element is Paper object
if __name__=='__main__':
    p = Pool()
    start = time.clock()
    papers = []
    for i in range(1, 15):
        papers.append(p.apply_async(get_papers, args=(i,)))
    p.close()
    p.join()
    end = time.clock()
    print('%.03f seconds for Step_1: Data downloading and reorgnization' % (end-start))
    # pdb.set_trace()
    ##### 2. count all the words in papers_global using reduce
    start = time.clock()
    papers = reduce(lambda x, y: x + y, [paper.get() for paper in papers])

    all_wordCount = reduce(data_Frame_sum, [paper.wordCount for paper in papers])
    end = time.clock()
    print('%.03f seconds for Step_2: Merge all wordCount into one DataFrame' % (end-start))

    topWords_plot(all_wordCount, 30)
    # pdb.set_trace()



# next step:
# 0. how to get the whole abstract, rather than part of it
# 2. pretty plot