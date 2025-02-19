import scrapy


class GroupSpider(scrapy.Spider):
    name = "group"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221/"]

    def parse(self, response):
        # response.encoding = 'utf-8'
        all_groups = response.css('a[href^="/group/"]')
        for group_link in all_groups:
            yield response.follow(group_link, callback=self.parse_group)

        next_page = response.xpath('//a[contains(text(), "Следующая")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_group(self, response):
        yield {
            'group_name': response.css('h2::text').get().strip(),
            'description': response.css('p.group_descr::text').get().strip(),
            'posts_count': int(response.css('div.posts_count::text').get().strip()[9:])
        }
