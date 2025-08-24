import json
import shutil
import sys
from pathlib import Path
from typing import Union

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.utils.regexTools import execMultiReSub
from src.loggers.simpleLogger import loggerPrint
from src.processers.injecters.injecterBase import InjecterBase
from src.processers.formatters.formatterBase import jsonPatternDict
from src.utils.fileTools import getAllFilesFromFolder, readJson


class JsonInjecter(InjecterBase):
    """
    desc: json 文件注入器
    """

    def __init__(self):
        super().__init__()

    def init(self, gameDataFolder: str, backupFolder: str = ""):
        return super().init(gameDataFolder, backupFolder)

    def inject(self, data: Union[str, dict[str, str]]) -> None:
        """
        desc: 根据翻译字典注入 json 文件
        params:
            data: 可以是翻译文件路径，也可以是翻译字典
        """
        super().inject(data)
        # 获取全部待翻译文件
        fileList: list[str] = getAllFilesFromFolder(self.gameDataFolder)
        # 逐文件匹配翻译并注入
        self._processFile(fileList=fileList)

    def _processFile(self, fileList: list[str]):
        processed_count = 0
        skipped_count = 0

        def __processSingleFile(file: str):
            """
            desc: 处理单个文件翻译注入
            params:
                file: 待翻译文件路径
            """
            fileContent: Union[dict, list] = readJson(file)
            translatedContent = __translateJsonData(fileContent)
            # 若数据无变化，则不写入，节省I/O
            if translatedContent == fileContent:
                # loggerPrint(f"文件 '{file}' 内容未改变，跳过写入。")
                nonlocal skipped_count
                skipped_count += 1
                return

            # 原子性写入：先写入临时文件，成功后再替换原文件
            # 这样可以防止在写入过程中程序崩溃导致文件损坏
            temp_file_path = file + ".tmp"
            with open(temp_file_path, "w", encoding="utf-8") as f:
                json.dump(translatedContent, f, ensure_ascii=False, indent=2)  # ensure_ascii=False 保留中文

            shutil.move(temp_file_path, file)
            # loggerPrint(f"文件 '{file}' 翻译完成并已更新。")
            nonlocal processed_count
            processed_count += 1

        def __translateJsonData(data: Union[dict, list, str]) -> Union[dict, list, str]:
            """
            desc: 递归遍历 json 数据结构，并根据翻译字典进行字符替换
            params:
                data: 待翻译数据
            """
            if isinstance(data, str):
                # 若为字符串，检查字符串是否在翻译字典的映射中
                return self.trDict.getTr(execMultiReSub(jsonPatternDict, data))
            if isinstance(data, list):
                # 若为列表，递归遍历子节点
                return [__translateJsonData(execMultiReSub(jsonPatternDict, item)) for item in data]
            if isinstance(data, dict):
                # 若为字典，递归遍历子节点
                return {k: __translateJsonData(execMultiReSub(jsonPatternDict, v)) for k, v in data.items()}
            return data

        for file in fileList:
            __processSingleFile(file)
        loggerPrint(f"JSON 文件注入完成。共处理 {processed_count} 个文件，跳过 {skipped_count} 个文件。")


if __name__ == "__main__":
    # 测试备份文件夹
    injecter = JsonInjecter()
    injecter.init(gameDataFolder="E:\\Games\\25-08-04\\エクリプスナイト・サーガver1_14\\www\\data")
    injecter._backupFolder()
    # 测试注入
    injecter.inject(
        "E:\\Games\\25-08-04\\エクリプスナイト・サーガver1_14\\extractData\\AiNieeOutput\\25-08-04_09-58_translated.json"
    )
