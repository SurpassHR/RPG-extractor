import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Extract data from RPG Maker game."
        )
        self._add_arguments()

    def _add_arguments(self):
        """
        Add arguments to the parser.
        """
        self.parser.add_argument(
            "--dataFolder", type=str, help="Path to the data folder"
        )
        self.parser.add_argument(
            "--outputFolder", type=str, help="Path to the output folder"
        )
        self.parser.add_argument(
            "--gui", action="store_true", help="Launch the GUI application"
        )

    def parse_args(self):
        """
        Parse command line arguments.
        """
        return self.parser.parse_args()
