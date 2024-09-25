import scrapy

class MonsterSpider(scrapy.Spider):
    name = 'monster_spider'
    start_urls = ['https://mhworld.kiranico.com/pt-BR/monsters']

    def parse(self, response):
        for monster in response.css('table.table-padded > tbody > tr'):
            url = monster.css('td div span a::attr(href)').get()
            if url:
                yield response.follow(url, self.parse_monster)

    def parse_monster(self, response):
        name = response.css('h5 > div > div.align-self-center::text').get().strip()
        description = response.css('div.col-sm-6::text').get().strip()
        table = response.css('div.table-responsive table.table')

        for row in table.css('tbody tr'):
            yield {
                'name': name,
                'description': description,
                'part': row.css('td:nth-child(1)::text').get(),
                'corte': row.css('td:nth-child(2)::text').get(),
                'contusao': row.css('td:nth-child(3)::text').get(),
                'a_distancia': row.css('td:nth-child(4)::text').get(),
                'fogo': row.css('td:nth-child(5)::text').get(),
                'agua': row.css('td:nth-child(6)::text').get(),
                'gelo': row.css('td:nth-child(7)::text').get(),
                'trovao': row.css('td:nth-child(8)::text').get(),
                'dragao': row.css('td:nth-child(9)::text').get(),
                'status': row.css('td:nth-child(10)::text').get(),
                'vigor': row.css('td:nth-child(11)::text').get()
            }
