from pathlib import Path
from src.processers.formatters.formatterBase import FormatterBase, jsonPatternDict
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.regexTools import execMultiReSub
from src.utils.dataStructTools import hashableListDedup


class JsonFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def _rmAllEscapes(self, dataList: list[str]) -> list[str]:
        subbedDataList: list[str] = []
        for item in dataList:
            data = execMultiReSub(jsonPatternDict, str(item))
            subbedDataList.append(data)

        return subbedDataList

    def format(self, data: list, debug: bool = False):
        """
        Formats the data list by removing escapes, deduplicating, and fixing line breaks.

        Args:
            data (list): The list of strings to format.
            debug (bool, optional): If True, saves intermediate files for debugging.
                                    Defaults to False.

        Returns:
            list: The formatted list.
        """
        # Process data sequentially
        res_no_escapes = self._rmAllEscapes(data)
        res_deduped = hashableListDedup(res_no_escapes)
        res_final = self._restoreIncorrectLineBreaks(res_deduped)

        # Dump intermediate files if debug mode is enabled
        if debug:
            timestamp = getCurrTimeInFmt("%y-%m-%d_%H-%M")
            output_dir = Path(f"output/formatter/json/{timestamp}")
            output_dir.mkdir(parents=True, exist_ok=True)

            dumpListToFile(res_no_escapes, str(output_dir / "textDisp_NoTitle.json"))
            dumpListToFile(res_deduped, str(output_dir / "textDisp_NoTitle_Dedup.json"))
            dumpListToFile(res_final, str(output_dir / "textDisp_NoTitle_Dedup_FixLineBreak.json"))
            self._setStageDataPath(str(output_dir / "textDisp_NoTitle_Dedup_FixLineBreak.json"))

        return res_final
