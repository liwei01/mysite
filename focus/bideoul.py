#coding=utf-8
'''
采集 http://www.biedoul.com/wenzi/ 的话
'''
import urllib, urllib2, re
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding( 'utf-8')

class Spider:
    def __init__(self):
        self.siteURL = 'http://www.biedoul.com/wenzi/'

    def getPage(self,pageIndex):
        url = self.siteURL + str(pageIndex) + '/'
        print url
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        #print response.read()
        return response.read()


    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        #print page
        #pattern = re.compile('<div.*?class=dzlist rmargin10">.*?<div.*?.*?<div.*?.*?<div.*?<a href=(.?)',re.S)
        pattern = re.compile('<div.*?class="dzlist-.*?>.*?<div.*?</div>.*?<div.*?<a.*?>(.*?)</a>.*?<div.*?</div>.*?<div.*?>.*?<a.*?<p.*?>(.*?)</p>.*?<p>(.*?)</p>',re.S)
        items = re.findall(pattern, page)
        print items
        conn = sqlite3.connect('db.sqlite3')
        print "Opened database successfully";
        for item in items:
            #print item[1].decode('utf-8'), item[2].decode('utf-8')
            #如何删除指定的字符串。'<br />'
            #item2 = item[2].replace('<br />', '')
            print item[0],item[1],item[2].replace('<br />', '')
            '''
            #保存到sqlite3
            '''
            d0 = item[0].decode('utf-8')
            d1 = item[1].decode('utf-8')
            d2 = item[2].replace('<br />', '').decode('utf-8')
            #conn.execute("INSERT INTO focus_article (title ,content ,author ) \
            #        VALUES (?,?,?)",(d1,d2,d0));
            conn.execute("INSERT INTO focus_article (title ,content ,pub_date,published,poll_num,comment_num,keep_num,author_id,column_id ) \
                    VALUES (?,?,'0','0','0','0','0','1','2')",(d1,d2));
        conn.commit()
        print "Records created successfully";
        conn.close()



spider = Spider()
#spider.getContents(1)

for i in range(10, 100):
    spider.getContents(i)
    print(i)
else:
    print('for循环结束')
