# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr']

    def parse(self, response):
        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()
            yield scrapy.Request(link, callback=self.parse_listing, meta={
                'date': date,
                'link': link,
                'text': text
            })
        next_page_url = response.xpath('//a[text()="next > "]/@href').extract_first()
        next_page_url = response.urljoin(next_page_url)
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_listing(self, response):
        date = response.meta['date']
        link = response.meta['link']
        text = response.meta['text']
        compensation = response.xpath('//*[@class="attrgroup"]/span[1]/b/text()').extract_first()
        type = response.xpath('//*[@class="attrgroup"]/span[2]/b/text()').extract_first()
        address = response.xpath('//*[@id="postingbody"]/text()').extract()

        yield {
            "date": date,
            "link": link,
            "text": text,
            "compensation": compensation,
            "type": type,
            "address": address
        }