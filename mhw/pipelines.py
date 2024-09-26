# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MhwPipeline:
    def process_item(self, item, spider):
        return item

class MonsterPipeline:
    def process_item(self, item, spider):
        for part in item['parts']:
            for key, value in part.items():
                if value is None:
                    part[key] = 'N/A'  # Atribui 'N/A' para valores faltantes
                elif key in ['corte', 'contusao', 'a_distancia', 'fogo', 'agua', 'gelo', 'trovao', 'dragao', 'status', 'vigor']:
                    part[key] = int(value) if value.isdigit() else 0  # Converte para inteiro ou atribui 0 se não for número

        return item
