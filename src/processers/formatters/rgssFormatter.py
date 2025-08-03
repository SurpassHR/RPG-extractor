from src.processers.formatters.formatterBase import FormatterBase


class RgssFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def format(self, data: dict) -> dict:
        return data
