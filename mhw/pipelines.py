# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import pandas as pd

class MhwPipeline:
    def process_item(self, item, spider):
        return item

class MonsterPipeline:
    part_translation = {
        'head': 'cabeça',
        'tail': 'cauda',
        'wing': 'asa',
        'claw': 'garra',
        # Adicione mais traduções conforme necessário
    }

    def process_item(self, item, spider):
        for part in item['parts']:
            part_name = part['part']
            if part_name in self.part_translation:
                part['part'] = self.part_translation[part_name]

            for key, value in part.items():
                if value is None:
                    part[key] = 'N/A'  # Atribui 'N/A' para valores faltantes
                elif key in ['corte', 'contusao', 'a_distancia', 'fogo', 'agua', 'gelo', 'trovao', 'dragao', 'status', 'vigor']:
                    part[key] = int(value) if value.isdigit() else 0  # Converte para inteiro ou atribui 0 se não for número

        return item

class MonsterVisualizationPipeline:
    def open_spider(self, spider):
        # Inicializa uma lista para armazenar os itens coletados
        self.data = []

    def process_item(self, item, spider):
        # Adiciona cada item processado na lista de dados
        self.data.append(item)
        return item

    def close_spider(self, spider):
        # Converte a lista de dados em um DataFrame do pandas
        all_monster_data = []
        for item in self.data:
            name = item['name']
            description = item['description']
            for part in item['parts']:
                # Adiciona o nome do monstro e a descrição em cada parte
                part_data = {
                    'name': name,
                    'description': description,
                    **part
                }
                all_monster_data.append(part_data)

        # Cria um DataFrame com os dados coletados
        df = pd.DataFrame(all_monster_data)

        # Salva os dados em um arquivo CSV
        df.to_csv('monsters.csv', index=False)
        spider.logger.info("Arquivo 'monsters.csv' salvo com sucesso.")
