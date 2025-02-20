import scrapy

from yatube_parsing.items import YatubeParsingItem


class YatubeSpider(scrapy.Spider):
    name = "yatube"
    allowed_domains = ["158.160.177.221"]
    start_urls = ["http://158.160.177.221"]

    def parse(self, response):
        for post in response.css('div.card-body'):
            yield YatubeParsingItem(
                {
                'author': '@' + post.css("p.card-text a::attr(href)").get().strip('/'),
                'text': ' '.join(post.css("p.card-text::text").getall()).strip(),
                'date': post.css("small.text-muted::text").get()
                }
            )
        next_page = response.css('ul.pagination').xpath('//li[last()]').css('a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# В примерах записано так:
# text = ' '.join(
#     t.strip() for t in post.css('p::text').getall()
# ).strip()