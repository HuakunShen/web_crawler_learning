# -*- coding: utf-8 -*-
import os, csv, glob
import mysql.connector as SQL
from scrapy import Spider
from scrapy.http import Request


def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()



class Booksdata4SqlSpider(Spider):
    name = 'booksData4_SQL'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # process next page
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        # price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        # description = response.xpath(
        #     '//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information data points
        upc = product_info(response, 'UPC')
        product_type =  product_info(response, 'Product Type')
        # price_without_tax = product_info(response, 'Price (excl. tax)')
        # price_with_tax = product_info(response, 'Price (incl. tax)')
        # tax = product_info(response, 'Tax')
        # availability = product_info(response, 'Availability')
        # number_of_reviews = product_info(response, 'Number of reviews')

        yield {
            'title': title,
            'rating': rating,
            'upc': upc,
            'product_type': product_type,
        }
    
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        print('debug, target file: ', csv_file)
        mydb = SQL.connect(host='localhost', user='huakun', password='', database='booksDB')
        cursor = mydb.cursor()
        with open(csv_file) as data_file:
            csv_data = csv.reader(data_file, delimiter=',')
            row_count = 0
            for row in csv_data:
                if row_count != 0:
                    query = ("INSERT IGNORE INTO books_table "
                   "(rating, product_type, upc, title) "
                   "VALUES (%s, %s, %s, %s)")
                    cursor.execute(query, row)
                row_count += 1
            print('debug: total row added = ', row_count)
    
        mydb.commit()
        cursor.close()
        mydb.close()