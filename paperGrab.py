from bs4 import BeautifulSoup
import re
import urllib2

class Papers():
    def __init__(self, title, abstract):
        self.title = title
        self.abstract = abstract

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

paper_titles = []
paper_abstracts = []
papers = []
for num in range(1,20):
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

i = 1
# for paper in papers:
#     print(str(i) + '. ' + paper )
for i in range(len(papers)):
    print str(i+1) + '. ' + papers[i].title + ':\nabstract: ' + papers[i].abstract + '\n'