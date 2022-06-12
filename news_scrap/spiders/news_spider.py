import os
import scrapy


class NewSpider(scrapy.Spider):
    name = "news"

    start_urls = [
        'https://vnexpress.net/khoa-hoc',
    ]


    def parse(self, response):
        for link in response.css('.title-news'):
            url = link.css('h3 a::attr(href)').get()
            if url is not None:
                yield scrapy.Request(url,self.parse_every_new)  
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
    


    def parse_every_new(self,response):
        dir = os.path.join('D:\\WEBSCRAWLING\\news_scrap\\news_scrap\\khoahoc\\')
        # filename = '%s.txt' % response.url.split('-')[-1][0:7]
        filename = '%s.txt' % response.css('body::attr(data-source)').get().split('-')[-1]
        filepath = os.path.join(dir,filename)
        title = response.css('h1.title-detail::text').get()
        description = response.css('p.description::text').get()
        f = open(filepath,'a+',encoding="utf-8")
        f.writelines('Title: ' + title + '\n')
        f.writelines('Description: ' + description + '\n')
        for data in response.css('p.Normal'):
            f.writelines(data.css('p::text').get())
        f.close()



           