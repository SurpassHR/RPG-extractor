from src.extractor import Extractor
from src.utils.configLoader import loadConfig
from src.utils.argParser import ArgParser

if __name__ == "__main__":
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    config = loadConfig()

    dataFolder: str = args.dataFolder or config.get("game_data_dir", "")
    outputFolder: str = args.outputFolder or config.get("output_data_dir", "")

    dataExtractor = Extractor(dataFolder=dataFolder, outputFolder=outputFolder)
    dataExtractor.extract()

    # jsFolder = os.path.join(dataFolder, '..', 'js')
    # jsExtractor = Extractor(
    #     dataFolder=jsFolder,
    #     outputFolder=outputFolder
    # )
    # jsExtractor.extract()
