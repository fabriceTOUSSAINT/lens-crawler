import scrapy
from scrapy.xlib.pydispatch import dispatcher

# Run this to export to json - scrapy runspider quotes_spider.py -o quotes.json

class dpSpider(scrapy.Spider):
    def __init__(self):
        dispatcher.connect(self.spider_closed, scrapy.signals.spider_closed)

    name = "lens"
    start_urls = [
            'https://www.dpreview.com/products/lenses/all?sort=alphabetical&view=grid',
        ]

    def spider_closed(self, spider):
        print 'SPIDER DONE ######'

    def parseSpecPage(self, response):
        print '<<<<<<<<<>>>>>>>>>>'
        lensData = response.meta['lensData']
        # lensData = {'lens_brand': response.css('meta[itemprop="brand"]').extract()}
        lensData['lens_brand'] = response.css('meta[itemprop="brand"]').extract()
        # 'focal_length':[],
        # 'f_stop_min':[],
        # 'f_stop_max':[],
        # 'sensor_size':[],

        # yield lensData
        yield lensData

    def parse(self, response):
        for lens in response.css('tr.products td.product'):
            # Fill up jawn object with details of lens on main page on by one
            jawn={
                'lens_name': lens.css('.name a::text').extract_first(),
                'lens_mount': lens.css('specs .shortProductSpecs::text').re(r'(?<=(\|\s))(.+?)(?=(\s\|)|$)'),
                # 'lens_mount': splitMount(lens.css('.specs .shortProductSpecs::text').extract_first()),
                'lens_type': lens.css('.specs .shortProductSpecs::text').re(r'^(.+?){1}(?=[\|])'),
                'dp_review_link': lens.css('.review a::attr(href)').extract_first(),
                'year_released': lens.css('.announcementDate::text').re(r'[a-zA-Z]+\s+\d{2},+\s+\d{4}'),
                'msrp': lens.css('.prices a::text').re(r'[0-9\,]+\.[0-9][0-9](?:[^0-9]|$)'),
                'dp_lens_detail_link': lens.css('.name a::attr(href)').extract(),
            }
        
            fullLensDetail = scrapy.Request(str(jawn['dp_lens_detail_link'][0]), callback=self.parseSpecPage)
            fullLensDetail.meta['lensData'] = jawn

            yield fullLensDetail

        print 'Also AT END'
