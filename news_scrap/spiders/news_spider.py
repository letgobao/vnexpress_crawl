
import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
class NewSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://vnexpress.net/khoa-hoc',
    ]
    rules = (
        Rule(LinkExtractor(unique=True))
    )
    follow_urls = []

    def parse(self, response):
        for link in response.css('.title-news'):
            url = link.css('h3 a::attr(href)').get()
            if url is not None and url not in self.follow_urls:
                self.follow_urls.append(url)
                yield scrapy.Request(url,self.parse_every_new)
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
    


    def parse_every_new(self,response):
        dir = os.path.join('D:\\WEBSCRAWLING\\news_scrap\\news_scrap\\khoahoc\\')
        filename = '%s.txt' %  response.css('meta::attr(content)')[8].get()
        filepath = os.path.join(dir,filename)
        title = response.css('title::text').get()
        keywords = response.css('meta::attr(content)')[1].get()
        description = response.css('meta::attr(content)')[0].get()
        create_at = response.css('span.date::text').get()
        author = response.css('p.Normal strong::text').get()
        source = response.css('p.Normal em::text').get()
        f = open(filepath,'a+',encoding="utf-8")
        f.writelines('Title: ' + title + '\n')
        f.writelines('Keywords: ' + keywords+ '\n')
        f.writelines('Description: ' + description + '\n')
        f.writelines('Create at: ' + create_at+ '\n')
        datas = response.css('p.Normal')
        datas.pop(-1)
        for data in datas:
            text = data.css('p::text').get()
            f.writelines(text)
            f.writelines('\n')
        f.writelines('Author: ' + author+ '\n')
        f.writelines('Source: ' + source+ '\n')
        f.close()



           