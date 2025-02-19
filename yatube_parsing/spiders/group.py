import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        all_groups = response.css('a[href^="/group/"]')
        for group_link in all_groups:
            print('=======================', group_link)
            yield response.follow(group_link)

        next_page = response.xpath('//a[contains(text(), "Следующая")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
