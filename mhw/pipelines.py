# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import os
import pandas as pd

class MhwPipeline:
    def process_item(self, item, spider):
        return item

class MonsterPipeline:
    def process_item(self, item, spider):
        for part in item['parts']:
            part_name = part['part']
            if not part_name:
                part['part'] = f'iceborne {part_name.strip()}'

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

        # Define uma lista de partes permitidas em inglês
        self.allowed_parts = ['Head', 'Neck', 'Tail', 'Body', 'Wings', 'Legs', 'Arms', 'Jaw', 'Back', 'Head Bone', 'Hindleg Bones', 'Left Bone', 'Right Bone']
        self.physiology_data = []
        self.breakability_data = []

    def process_item(self, item, spider):
        filtered_parts = []
        
        for part in item['parts']:
            # Converte os valores que devem ser numéricos para um array
            numerical_values = [
                part.get('corte', 0),
                part.get('contusao', 0),
                part.get('a_distancia', 0),
                part.get('fogo', 0),
                part.get('agua', 0),
                part.get('gelo', 0),
                part.get('trovao', 0),
                part.get('dragao', 0),
                part.get('status', 0),
                part.get('vigor', 0)
            ]
            
            # Verifica se todos os valores numéricos são zero
            if any(value != 0 for value in numerical_values):
                filtered_parts.append(part)

        # Se houver partes válidas (não totalmente zeradas), adiciona o item
        if filtered_parts:
            item['parts'] = filtered_parts
            self.data.append(item)

        # Separar os dados de physiology e de part breakability
        physiology = item.get('physiology')
        if physiology:
            self.physiology_data.append(physiology)

        breakability = item.get('breakability')
        if breakability:
            self.breakability_data.append(breakability)

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

        # Cria DataFrames com os dados coletados
        df_monsters = pd.DataFrame(all_monster_data)
        df_physiology = pd.DataFrame(self.physiology_data)
        df_breakability = pd.DataFrame(self.breakability_data)

        # Define o caminho para o diretório fora do projeto
        output_directory = '/home/yuri/monsters_csv'

        # Verifica se o diretório já existe, se não, cria o diretório
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Define o caminho completo dos arquivos CSV
        file_monsters = os.path.join(output_directory, 'monsters.csv')
        file_physiology = os.path.join(output_directory, 'physiology.csv')
        file_breakability = os.path.join(output_directory, 'breakability.csv')

        # Salva os dados em arquivos CSV
        df_monsters.to_csv(file_monsters, index=False)
        df_physiology.to_csv(file_physiology, index=False)
        df_breakability.to_csv(file_breakability, index=False)

        spider.logger.info(f"Arquivo 'monsters.csv' salvo com sucesso em {file_monsters}")
        spider.logger.info(f"Arquivo 'physiology.csv' salvo com sucesso em {file_physiology}")
        spider.logger.info(f"Arquivo 'breakability.csv' salvo com sucesso em {file_breakability}")
