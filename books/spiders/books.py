import scrapy


"""
# response.xpath(
            # '//div[@class="content__main-column content__main-column--article js-content-main-column "]//p/text()').extract()
                New York Times
response.xpath('//h2[@class="story-heading"]/a/@href').extract()
response.xpath('//a[@class="story-link"]/@href').extract()

                Guardian
                
response.xpath('//a[@class="fc-item__link"]/@href').extract()
response.xpath('//a[@class="u-faux-block-link__overlay js-headline-text"]/@href').extract()

                Deutche welle
 response.xpath('//div[@class="news searchres"]/a/@href').extract()
 response.xpath('//div[@class="imgTeaserM white below"]/a/@href')[0].extract()
 response.xpath('//div[@class="news"]/a/@href').extract()

 'http://www.dw.com/en/top-stories/s-9097',
 'https://www.theguardian.com/international',

 'dw.com/en/top-stories/s-9097/',
 'theguardian.com/international/',
"""

class QuotesSpider(scrapy.Spider):
    name = "books"
    counter = 0
    def start_requests(self):
        
        urls = [
            'https://www.theguardian.com/international/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.init)

    def init(self, response):
        page = response.url.split("/")[-2]
        filename = 'news-%s.txt' % page
        text = response.xpath('//a[@class="fc-item__link"]/@href').extract()
        # text = ''.join(text)
        text2 = response.xpath('//a[@class="u-faux-block-link__overlay js-headline-text"]/@href').extract()
        text += text2
        # text = ''.join(text)
        for i in text:
            yield scrapy.Request(url=i, callback=self.parse_next)
        # with open(filename, 'w') as f:
        #     f.write(text)
        self.log('Saved file %s' % filename)

    def parse_next(self, response):
        url_ = response.request.url
        text =[]
        text.append("url:%s \n" % url_)
        text += response.xpath("/html").extract()
        title = response.xpath('//h1[@class="content__headline "]/text()').extract()
        if  len(title)!=0:
            # self.counter += 1
            filename = '%s.html' % title[0].strip('\n')
            text = ''.join(text)
            text=text.encode("utf8")
            with open(filename, 'w') as f:
                f.write(text)
