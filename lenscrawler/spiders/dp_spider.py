import scrapy

# Run this to export to json - scrapy runspider dp_spider.py -o lensData.json

class dpSpider(scrapy.Spider):
    name = "lens"
    start_urls = [
            'https://www.dpreview.com/products/lenses/all?sort=alphabetical&view=grid',
        ]

    def parseSpecPage(self, response):
        lensData = response.meta['lensData']
        lensData['lens_brand'] = response.css('meta[itemprop="brand"]::attr(content)').extract_first()

        for spec in response.css('div.quickSpecs tr'):
            currSpec = spec.css('td.label::text').extract_first()

            if currSpec == 'Lens type':
                lensData['lens_type'] = spec.css('td.value::text').extract_first()
            elif currSpec == 'Focal length':
                lensData['focal_length'] = spec.css('td.value::text').extract_first()
            elif currSpec == 'Max aperture':
                lensData['f_stop_max'] = spec.css('td.value::text').extract_first()
            elif currSpec == 'Min aperture':
                lensData['f_stop_min'] = spec.css('td.value::text').extract_first()
            elif currSpec == 'Lens mount':
                lensData['lens_mount'] = spec.css('td.value::text').extract_first()

        yield lensData

    def parse(self, response):
        for lens in response.css('tr.products td.product'):
            # Fill up shallowLensData object with details of lens on main page on by one
            shallowLensData={
                'lens_name': lens.css('.name a::text').extract_first(),
                'lens_type': lens.css('.specs .shortProductSpecs::text').re(r'^(.+?){1}(?=[\|])'),
                'dp_review_link': lens.css('.review a::attr(href)').extract_first(),
                'year_released': lens.css('.announcementDate::text').re(r'[a-zA-Z]+\s+\d{2},+\s+\d{4}'),
                'msrp': lens.css('.prices a::text').re(r'[0-9\,]+\.[0-9][0-9](?:[^0-9]|$)'),
                'dp_lens_detail_link': lens.css('.name a::attr(href)').extract_first(),
            }
        
            fullLensDetail = scrapy.Request(shallowLensData['dp_lens_detail_link'], callback=self.parseSpecPage)
            fullLensDetail.meta['lensData'] = shallowLensData

            yield fullLensDetail

