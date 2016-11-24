from bs4 import BeautifulSoup
import re
import urllib2

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
pattern_abstract = re.compile(r'<p>[\s]*(.*?)[\s]*<a href="/document')
paper_titles = []
paper_abstracts = []
for num in range(1,2):
    print('page ' + str(num) + ' start, wait...')

    for title in content_grab(pageNum=num, pattern=pattern_title):
      paper_titles.append(title)

    for abstract in content_grab(pageNum=num, pattern=pattern_abstract):
      paper_abstracts.append(abstract)

    print('page ' + str(num) + ' finished.')

i = 1
for title in paper_titles:
    print str(i) + '. ' + title
    i = i + 1
print '\n'

i = 1
for abstract in paper_abstracts:
    print str(i) + '. ' + abstract
    i = i + 1