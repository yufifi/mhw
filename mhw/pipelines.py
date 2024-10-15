import os
import pandas as pd

class MonsterPipeline:
    allowed_parts = [
        'Head', 'Neck', 'Left Leg', 'Right Leg', 'Tail', 'Body', 'Wings', 
        'Legs', 'Arms', 'Jaw', 'Back', 'Torso', 'Leg', 'Nose', 'Left Foreleg', 
        'Right Foreleg', 'Left Hindleg', 'Right Hindleg', 'Forelegs'
    ]

    def process_item(self, item, spider):
        filtered_parts = []

        for part in item['parts']:
            part_name = part['part']

            if part_name in self.allowed_parts:
                for key, value in part.items():
                    if value is None:
                        part[key] = 'iceborne ' + part_name  # Substitui valores vazios
                    elif key in ['corte', 'contusao', 'a_distancia', 'fogo', 'agua', 'trovao', 'gelo', 'dragao', 'atordoamento', 'vigor']:
                        part[key] = int(value) if isinstance(value, str) and value.isdigit() else value or 0

                filtered_parts.append(part)

        if filtered_parts:
            item['parts'] = filtered_parts
        else:
            item['parts'] = []

        return item

class MonsterVisualizationPipeline:
    def open_spider(self, spider):
        self.data = []
        self.physiology_data = []

    def process_item(self, item, spider):
        filtered_parts = []

        for part in item['parts']:
            numerical_values = [
                part.get('corte', 0),
                part.get('contusao', 0),
                part.get('a_distancia', 0),
                part.get('fogo', 0),
                part.get('agua', 0),
                part.get('trovao', 0),
                part.get('gelo', 0),
                part.get('dragao', 0),
                part.get('atordoamento', 0),
                part.get('vigor', 0)
            ]

            if any(value != 0 for value in numerical_values):
                filtered_parts.append(part)

                # Dados de fisiologia
                physiology = {
                    'name': item['name'],
                    'part': part['part'],
                    'corte': part.get('corte', 0),
                    'contusao': part.get('contusao', 0),
                    'a_distancia': part.get('a_distancia', 0),
                    'fogo': part.get('fogo', 0),
                    'agua': part.get('agua', 0),
                    'trovao': part.get('trovao', 0),
                    'gelo': part.get('gelo', 0),
                    'dragao': part.get('dragao', 0),
                    'atordoamento': part.get('atordoamento', 0),
                    'vigor': part.get('vigor', 0)
                }
                self.physiology_data.append(physiology)

        if filtered_parts:
            item['parts'] = filtered_parts
            self.data.append(item)

        return item

    def close_spider(self, spider):
        all_monster_data = []
        for item in self.data:
            name = item['name']
            description = item.get('description', '')
            for part in item['parts']:
                part_data = {
                    'name': name,
                    'description': description,
                    **part
                }
                all_monster_data.append(part_data)

        df_monsters = pd.DataFrame(self.data, columns=['name', 'description'])
        df_physiology = pd.DataFrame(self.physiology_data)

        output_directory = '/home/yuri/monsters_csv'

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        file_path_monsters = os.path.join(output_directory, 'monsters.csv')
        file_path_physiology = os.path.join(output_directory, 'physiology.csv')

        # Reordena colunas de physiology.csv
        columns_order_physiology = ['name', 'part', 'corte', 'contusao', 'a_distancia', 'fogo', 'agua', 'trovao', 'gelo', 'dragao', 'atordoamento', 'vigor']
        df_physiology = df_physiology[columns_order_physiology]

        df_monsters.to_csv(file_path_monsters, index=False)
        df_physiology.to_csv(file_path_physiology, index=False)

        spider.logger.info("Arquivos 'monsters.csv' e 'physiology.csv' salvos com sucesso.")

