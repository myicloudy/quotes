# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuotetutorialItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuotetutorialItem()
            text = quote.css('.text::text').extract_first()   # 只有一个内容用extract_first
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()  # 多个内容用extract
            item['author'] = author
            item['text'] = text
            item['tags'] = tags
            yield item

        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)