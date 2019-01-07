import re

from urllib import request

class Spider():
    url = 'http://d81fb43e-d.parkone.cn'

    # 书链接的父级
    book_pattern = '<div class="cover">([\s\S]*?)</div>'

    # 获取书的链接
    book_pattern1 = '<a href="([\s\S]*?)" data-toggle="modal" data-target="#bookDetailsModal" data-remote="false">'
   
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


    # 通过链接找到页面相关信息的方法
    def __fetch_content(self, url):
        resp = request.urlopen(url)
        htmls = resp.read()
        htmls = str(htmls, encoding='utf-8')

        return htmls


    # 找到书籍链接的方法
    def __find_url(self, htmls):
        # 通过书链接父级标签找到所有关于书的html
        root = re.findall(Spider.book_pattern, htmls)
        book_urls = []
        for i in root:
            book_url = re.findall(Spider.book_pattern1, i)
            # 每一本书的链接
            new_url = Spider.url + book_url[0]
            # 将每本书的url添加到新的列表中
            book_urls.append(new_url)

        return book_urls


    # 爬书方法
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

    def __show(self, anchors):
        for book in anchors:
            print('书名' + str(book['书名']))
            print('作者' + str(book['作者']))
            print('出版社' + str(book['出版社']))
            print('出版日期' + str(book['出版日期']))
            print('简介' + str(book['简介']))
            print('-----------------------------------------------------------')

    def go(self):
        i = 1
        while True:
            page_url = 'http://d81fb43e-d.parkone.cn/page/{}'.format(str(i))
            htmls = self.__fetch_content(page_url)
            book_urls = self.__find_url(htmls)
            if len(book_urls) != 0:
                for url in book_urls:
                    html = self.__fetch_content(url)
                    anchors = self.__analysis(html)
                    self.__show(anchors)
                i += 1
            else:
                break

spider = Spider()
spider.go()