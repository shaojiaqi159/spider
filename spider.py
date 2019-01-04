import re

from urllib import request

class Spider():

    url = 'http://d81fb43e-d.parkone.cn/book/'
    #书名
    bookname_pattern = '<h2>([\s\S]*?)</h2>'
    #作者
    author_pattern = '<a href="/author/[\s\S]*?">([\s\S]*?)</a>'
    #出版社
    press_pattern = '<span>出版社:([\s\S]*?)</span>'
    #简介
    brief_pattern = '<p class="description">([\s\S]*?)</p>'
    #出版日期
    publication_pattern = '<p>出版日期:([\s\S]*?)</p>'

    def __fetch_content(self, i):
        url = Spider.url+str(i)
        r = request.urlopen(url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls
              
    def __analysis(self, htmls):
        anchors = []
        bookname = re.findall(Spider.bookname_pattern, htmls)
        author = re.findall(Spider.author_pattern, htmls)
        press = re.findall(Spider.press_pattern, htmls) 
        publication = re.findall(Spider.publication_pattern, htmls)
        brief = re.findall(Spider.brief_pattern, htmls)

        anchor = {'书名':bookname, '作者':author, '出版社':press, '出版日期':publication,'简介':brief}
        anchors.append(anchor)
        return anchors

    def go(self, i):
        htmls = self.__fetch_content(i) 
        anchors = self.__analysis(htmls)
        print(anchors)

for i in range(1,254):
    spider = Spider()
    spider.go(i)