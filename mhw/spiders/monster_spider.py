import scrapy

class MonsterSpider(scrapy.Spider):
    name = 'monster_spider'
    start_urls = ['https://mhworld.kiranico.com/pt-BR/monsters']

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
    }

    def parse(self, response):
        self.logger.info("Iniciando a coleta de monstros...")
        
        # Extrai a lista de monstros e segue os links para as páginas detalhadas
        for monster in response.css('table.table-padded > tbody > tr'):
            url = monster.css('td div span a::attr(href)').get()
            name = monster.css('td div span a::text').get()
            
            if url:
                self.logger.debug(f"Seguindo o link do monstro: {name} - {url}")
                yield response.follow(url, self.parse_monster)
            else:
                self.logger.warning(f"Nenhum URL encontrado para o monstro: {name}")

    def parse_monster(self, response):
        # Extrai nome e descrição do monstro
        name = response.css('div.align-self-center::text').get()
        if name:
            name = name.strip()
        else:
            self.logger.warning("Nome do monstro não encontrado.")

        description = response.css('div.col-sm-6::text').get()
        if description:
            description = description.strip()
        else:
            self.logger.warning(f"Descrição não encontrada para o monstro: {name}")

        # Captura as tabelas de fisiologia para diferentes elementos
        elements = ["Fire", "Ice", "Dragon", "No Element"]
        physiology_data = []

        for element in elements:
            self.logger.debug(f"Capturando fisiologia para o elemento: {element}")
            table = response.xpath(f'//h6[contains(text(), "Fisiologia")]/following-sibling::div[@class="table-responsive"][1]')
            if not table:
                self.logger.warning(f"Tabela de fisiologia não encontrada para o elemento: {element}")
                continue
            
            # Processa as partes do corpo e suas resistências para o elemento atual
            for row in table.css('tbody tr'):
                part = row.css('td:nth-child(1)::text').get()
                if part:
                    part_data = {
                        'part': part.strip(),
                        'element': element,  # Adiciona o elemento atual ao dicionário
                        'corte': (row.css('td:nth-child(2)::text').get() or '').strip(),
                        'contusao': (row.css('td:nth-child(3)::text').get() or '').strip(),
                        'a_distancia': (row.css('td:nth-child(4)::text').get() or '').strip(),
                        'fogo': (row.css('td:nth-child(5)::text').get() or '').strip(),
                        'agua': (row.css('td:nth-child(6)::text').get() or '').strip(),
                        'trovao': (row.css('td:nth-child(7)::text').get() or '').strip(),
                        'gelo': (row.css('td:nth-child(8)::text').get() or '').strip(),
                        'dragao': (row.css('td:nth-child(9)::text').get() or '').strip(),
                        'atordoamento': (row.css('td:nth-child(10)::text').get() or '').strip(),
                        'vigor': (row.css('td:nth-child(11)::text').get() or '').strip(),
                    }
                    physiology_data.append(part_data)

        if physiology_data:
            self.logger.debug(f"Fisiologia extraída para o monstro: {name}")
        else:
            self.logger.warning(f"Nenhuma parte de fisiologia encontrada para o monstro: {name}")

        yield {
            'name': name,
            'description': description,
            'physiology': physiology_data  # Dados de fisiologia completos, incluindo múltiplos elementos
        }

