import json

class Exporter:
    def __init__(self):
        pass

    def exportDictToJson(self, data: dict, exportJson: str):
        with open(exportJson, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

    def exportListToJson(self, data: list, exportJson: str):
        jsonContent: dict = {}
        for item in data:
            key = val = f'{item}'
            jsonContent[key] = val

        self.exportDictToJson(jsonContent, exportJson)

    def exportToRb(self, data: list, exportRb: str):
        with open(exportRb, 'w') as rbFile:
            for item in data:
                rbFile.write('{}'.format(item.replace('\r', '')))

if __name__ == '__main__':
    exporter = Exporter()
    exporter.exportListToJson(['example1', 'example2'], 'export.json')