from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import loggerPrint
from src.utils.configLoader import loadConfig
from src.utils.argParser import ArgParser
from src.proc import Proc


def main():
    arg_parser = ArgParser()
    args = arg_parser.parse_args()

    config = loadConfig()
    dataFolder: str = args.dataFolder or config.get("game_data_dir", "")
    outputFolder: str = args.outputFolder or config.get("output_data_dir", "")

    title: str = args.title
    format: bool = args.format

    if args.gui:
        from gui_template.app.app import startApp
        startApp()
    else:
        if args.extract:
            dataExtractor = Proc(dataFolder=dataFolder, outputFolder=outputFolder, title=title, format=format, mode=Proc.ProcMode.Extract)
            # 启用实验性功能: rgss 读取器读取文件内容
            if args.rgss:
                dataExtractor.initRgssReader()
            dataExtractor.proc()
        elif args.inject:
            dataExtractor = Proc(dataFolder=dataFolder, outputFolder=outputFolder, title=title, mode=Proc.ProcMode.Inject)
            dataExtractor.proc()
        else:
            loggerPrint(msg="No action specified, use --extract or --inject.", level=LogLevels.CRITICAL)


if __name__ == "__main__":
    main()
