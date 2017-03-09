import scrapy
import pdb

class dpSpider(scrapy.Spider):
    name = "lens"
    start_urls = [
            'https://www.dpreview.com/products/lenses/all?sort=alphabetical&view=grid',
        ]

    def parse(self, response):
        for lens in response.css('tr.products td.product'):
            yield {
                'lens_name': lens.css('.name a::text').extract_first(),
                'lens_brand':[],
                'lens_mount': lens.css('specs .shortProductSpecs::text').re(r'(?<=(\|\s))(.+?)(?=(\s\|)|$)'),
                # 'lens_mount': splitMount(lens.css('.specs .shortProductSpecs::text').extract_first()),
                'lens_type': lens.css('.specs .shortProductSpecs::text').re(r'^(.+?){1}(?=[\|])'),
                'focal_length':[],
                'f_stop_min':[],
                'f_stop_max':[],
                'sensor_size':[],
                'dp_review_link': lens.css('.review a::attr(href)').extract_first(),
                'year_released': lens.css('.announcementDate::text').re(r'[a-zA-Z]+\s+\d{2},+\s+\d{4}'),
                'msrp': lens.css('.prices a::text').re(r'[0-9\,]+\.[0-9][0-9](?:[^0-9]|$)'),
                'dp_lens_detail_link': lens.css('.name a::attr(href)').extract(),
            }
