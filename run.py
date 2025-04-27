import os
from src.extractor import Extractor
from src.utils.configLoader import loadConfig

if __name__ == '__main__':
    config = loadConfig()

    dataFolder: str = config.get('game_data_dir', '')
    outputFolder: str = config.get('output_data_dir', '')

    # dataExtractor = Extractor(
    #     dataFolder=dataFolder,
    #     outputFolder=os.path.join(outputFolder, 'data')
    # )
    # dataExtractor.extract()

    jsFolder = os.path.join(dataFolder, '..', 'js')
    jsExtractor = Extractor(
        dataFolder=jsFolder,
        outputFolder=os.path.join(outputFolder, 'js')
    )
    jsExtractor.extract()