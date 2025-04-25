import src.loggers
from src.extractor import Extractor
from src.utils.configLoader import loadConfig

if __name__ == '__main__':
    config = loadConfig()
    extractor = Extractor(
        dataFolder=config.get('game_data_dir'),
        outputFolder=config.get('output_files')
    )
    extractor.extract()