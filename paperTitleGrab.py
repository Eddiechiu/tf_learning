from bs4 import BeautifulSoup
import re
import urllib.request

def title_grab(page_num,pattern):
    url = 'http://ieeexplore.ieee.org/xpl/mostRecentIssue.jsp?...' \
          'punumber=77&filter%3DAND%28p_IS_Number%3A7368234%29&pageNumber=' + str(page_num)
    headers = ('User-Agent', 'Mozilla/5.0...'
                         ' (Windows NT 10.0; Win64; x64)...'
                         ' AppleWebKit/537.36 (KHTML, like Gecko)...'
                         ' Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586')
    urlopener = urllib.request.build_opener()
    urlopener.addheaders = [headers]
    data = urlopener.open(url).read()
    data = data.decode('GBK')
    return pattern.findall(data)

pattern = re.compile(r'<span id="art-abs-title-\d{7}">(.*?)</span>')
paper_titles = []

for num in range(1, 2):
    print('page ' + str(num) + ' start, wait...')
    for title in title_grab(page_num=num, pattern=pattern):
      paper_titles.append(title)
    print('page ' + str(num) + ' finished.')

for title in paper_titles:
    print(title)
