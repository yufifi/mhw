import scrapy

class MonsterSpider(scrapy.Spider):
    name = 'monster_spider'
    start_urls = ['https://mhworld.kiranico.com/pt-BR/monsters']
    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        for monster in response.css('table.table-padded > tbody > tr'):
            url = monster.css('td div span a::attr(href)').get()
            if url:
                yield response.follow(url, self.parse_monster)

    def parse_monster(self, response):
        name = response.css('h5 > div > div.align-self-center::text').get()
        description = response.css('div.col-sm-6::text').get()

        if name is None or description is None:
            self.logger.error(f"Nome ou descrição não encontrado para a URL: {response.url}")
            return

        name = name.strip()
        description = description.strip()
        
        table = response.css('div.table-responsive table.table')
        parts_data = []

        for row in table.css('tbody tr'):
            part = row.css('td:nth-child(1)::text').get()
            if part:
                part_data = {
                    'part': part.strip,
                    'corte': row.css('td:nth-child(2)::text').get().strip(),
                    'contusao': row.css('td:nth-child(3)::text').get().strip(),
                    'a_distancia': row.css('td:nth-child(4)::text').get().strip(),
                    'fogo': row.css('td:nth-child(5)::text').get().strip(),
                    'agua': row.css('td:nth-child(6)::text').get().strip(),
                    'gelo': row.css('td:nth-child(7)::text').get().strip(),
                    'trovao': row.css('td:nth-child(8)::text').get().strip(),
                    'dragao': row.css('td:nth-child(9)::text').get().strip(),
                    'status': row.css('td:nth-child(10)::text').get().strip(),
                    'vigor': row.css('td:nth-child(11)::text').get().strip()
                }
                parts_data.append(part_data)
            else:
                self.logger.error(f"Parte não encontrada na URL: {response.url}")

        if parts_data:
            yield{
                'name': name.strip(),
                'description': description.strip(),
                'parts': parts_data
            }
        else:
            self.logger.warning(f"Nenhuma parte encontrada para o monstro: {name}")
