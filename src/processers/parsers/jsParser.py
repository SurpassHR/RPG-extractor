import json
import re

from src.processers.parsers.parserBase import ParserBase
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer
from src.utils.dataStructTools import getAtomObjFromObj


class JsParser(ParserBase):
    def __init__(self):
        super().__init__()

    def _getTargetFileKeyContent(self, data: str) -> str:
        if not data:
            return ""

        pattern = re.compile(r"var \$plugins =\n*(\[.*\])", flags=re.DOTALL)  # re.S 包含回车换行
        res = re.findall(pattern, data)
        if not res or len(res) == 0:
            return ""

        return res[0]

    def _deepParse(self, data):
        # 处理字典类型
        if isinstance(data, dict):
            return {k: self._deepParse(v) for k, v in data.items()}

        # 处理列表类型
        if isinstance(data, list):
            return [self._deepParse(item) for item in data]

        # 处理字符串类型
        if isinstance(data, str):
            # 尝试解析字符串为JSON
            try:
                # 先移除字符串首尾空白（根据实际需求决定是否保留）
                stripped = data.strip()
                parsed = json.loads(stripped)
                # 递归处理解析后的结果
                return self._deepParse(parsed)
            except json.JSONDecodeError:
                # 解析失败时保留原始字符串
                # 可以在此处添加额外的转义处理逻辑
                return data

        # 其他类型直接返回
        return data

    @timer
    def parse(self, data: str) -> list:
        """
        从原始JS文件中解析插件列表。

        Args:
            data: 包含插件列表的JS文件内容。

        Returns:
            解析和处理后的插件列表。
        """
        target_content = self._getTargetFileKeyContent(data)
        if not target_content:
            # 在未找到目标内容时返回空列表，而不是引发错误
            return []

        try:
            plugin_list = json.loads(target_content)
        except json.JSONDecodeError:
            # 处理无效的JSON数据
            # 可以在此处添加日志记录
            return []

        # 移除调试文件转储，以提高清晰度和性能
        dumpListToFile(plugin_list, f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList.json")

        # 将处理步骤合并到一个循环中
        processed_list = []
        for item in plugin_list:
            # 检查item是否为非空字符串且以 "{" 或 "[" 开头
            if isinstance(item, str) and item and item.strip().startswith(("{" or "[")):
                processed_list.append(self._deepParse(item))
            else:
                processed_list.append(item)

        # 最终的原子对象提取
        final_list = getAtomObjFromObj(processed_list)

        # 移除调试文件转储
        stageDataPath = f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_final.json"
        dumpListToFile(final_list, stageDataPath)

        self._setStageDataPath(stageDataPath)

        return final_list
