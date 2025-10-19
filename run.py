from src.proc import Proc
from src.utils.configLoader import loadConfig
from src.utils.argParser import ArgParser


def main():
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    if args.gui:
        from gui_template.app.app import startApp

        startApp()

    else:
        if args.extract:
            config = loadConfig()
            dataFolder: str = args.dataFolder or config.get("game_data_dir", "")
            outputFolder: str = args.outputFolder or config.get("output_data_dir", "")

            title: str = args.title
            format: bool = args.format

            dataExtractor = Proc(dataFolder=dataFolder, outputFolder=outputFolder, title=title, format=format)
            dataExtractor.extract()
        elif args.inject:
            pass


if __name__ == "__main__":
    main()
