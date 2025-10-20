import argparse
from collections.abc import Sequence


class ArgParser:
    parser: argparse.ArgumentParser

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Extract data from RPG Maker game.")
        self._add_arguments()

    def _add_arguments(self):
        """
        向参数解析器中增添新的参数
        """
        # 通用参数
        _ = self.parser.add_argument("--dataFolder", type=str, help="Path to the data folder.")
        _ = self.parser.add_argument("--outputFolder", type=str, help="Path to the output folder.")

        # 开发参数
        _ = self.parser.add_argument("--rgss", action="store_true", help="Use the developing rgss reader for rubymarshall reader.")

        # 提取参数
        _ = self.parser.add_argument("--extract", action="store_true", help="Instruct the script to perform the extraction.")
        _ = self.parser.add_argument("--title", type=str, help="Title of the game.")
        _ = self.parser.add_argument("--format", action="store_true", help="Format data or use raw data.")

        _ = self.parser.add_argument("--inject", action="store_true", help="Instruct the script to perform the injection.")
        _ = self.parser.add_argument("--trFolder", type=str, help="Path to the translation folder.")

        # GUI参数
        _ = self.parser.add_argument("--gui", action="store_true", help="Launch the GUI application.")

    def parse_args(self,):
        """
        解析命令行参数
        """
        return self.parser.parse_args()
