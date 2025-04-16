import re
from typing import List, Dict, Union
from rubymarshal.classes import RubyObject

class RubyObjFormatter:
    def __init__(self) -> None:
        pass

    def parseRubyObj(self, rubyObj: RubyObject) -> Dict[str, Union[List[str], int, None]]:
        ruby_obj_str = str(rubyObj)
        # 正则匹配 @parameters, @indent, @code
        param_pattern = r"'@parameters': \[(b?['\"].*?['\"])\]"
        indent_pattern = r"'@indent': (\d+)"
        code_pattern = r"'@code': (\d+)"

        params = []
        for match in re.finditer(param_pattern, ruby_obj_str):
            param = match.group(1)
            if param.startswith('b'):
                param = eval(param).decode('utf-8')  # 注意：eval 有安全风险，仅限可信数据！
            else:
                param = param.strip('\'"')
            params.append(param)

        indent_match = re.search(indent_pattern, ruby_obj_str)
        code_match = re.search(code_pattern, ruby_obj_str)

        return {
            '@parameters': params,
            '@indent': int(indent_match.group(1)) if indent_match else None,
            '@code': int(code_match.group(1)) if code_match else None,
        }

    # 判断前后两个字符串是否需要合并
    def needsMerge(self, rubyStr1: str, rubyStr2: str) -> bool:
        # 检查 str1 是否有未闭合的 '(' 或 '['
        hasUnclosedParen = ('(' in rubyStr1 and ')' not in rubyStr1) or ('[' in rubyStr1 and ']' not in rubyStr1)

        # 检查 str2 是否有未闭合的 ')' 或 ']'
        hasUnclosedEnd = (')' in rubyStr2 and '(' not in rubyStr2) or (']' in rubyStr2 and '[' not in rubyStr2)

        return hasUnclosedParen and hasUnclosedEnd

    def mergeRubyObjects(self, obj1: Dict, obj2: Dict) -> Dict:
        mergedText = obj1['@parameters'][0] + obj2['@parameters'][0]
        return {
            '@parameters': [mergedText],
            '@indent': obj1['@indent'],
            '@code': obj1['@code'],
        }

    def processRubyObjList(self, rubyObjList: List[RubyObject]) -> List[RubyObject]:
        if not rubyObjList:
            return []

        parsed_objs = [self.parseRubyObj(obj) for obj in rubyObjList]
        merged_objs = []
        i = 0
        n = len(parsed_objs)

        while i < n:
            current_obj: dict = parsed_objs[i]
            if i < n - 1:
                next_obj: dict = parsed_objs[i + 1]
                # 检查是否需要合并
                if (current_obj['@indent'] == next_obj['@indent'] and  # 确保 indent 相同
                    len(current_obj['@parameters']) == 1 and  # 确保只有一个参数
                    len(next_obj['@parameters']) == 1 and
                    self.needsMerge(current_obj['@parameters'][0], next_obj['@parameters'][0])):
                    # 合并
                    merged_obj = self.mergeRubyObjects(current_obj, next_obj)
                    merged_objs.append(merged_obj)
                    i += 2  # 跳过下一个对象，因为已经合并
                    continue

            # 不需要合并，直接添加
            merged_objs.append(current_obj)
            i += 1

        # 重新生成 RubyObject 字符串
        result = []

        def __regenRubyObj(paramBytes: str, indent: int, code: int):
            param_bytes = f"b{repr(param.encode('utf-8'))}"
            ruby_obj_str = f"RubyObject({{'@parameters': [{param_bytes}], '@indent': {obj['@indent']}, '@code': {obj['@code']}}})"
            result.append(ruby_obj_str)

        for obj in merged_objs:
            param = ''
            if not obj['@parameters']:
                __regenRubyObj('', obj['@indent'], obj['@code'])
            else:
                __regenRubyObj(repr(param.encode('utf-8')), obj['@indent'], obj['@code'])

        return result

# 示例用法
if __name__ == "__main__":
    # 输入数据（包含多个 RubyObject，其中部分需要合并）
    rubyObjList = [
        RubyObject(attributes={'@parameters': [b"(Even though I said I'm not his woman, but I somehow "], '@indent': 3, '@code': 401}),
        RubyObject(attributes={'@parameters': [b'have the opposite emotion...)'], '@indent': 3, '@code': 401}),
        RubyObject(attributes={'@parameters': [b"[This is another sentence"], '@indent': 2, '@code': 402}),
        RubyObject(attributes={'@parameters': [b" that should not be merged]"], '@indent': 2, '@code': 402}),
        RubyObject(attributes={'@parameters': [b"Hello world"], '@indent': 1, '@code': 200}),
    ]

    print("原始列表:")
    for obj in rubyObjList:
        print(obj)

    rubyObjFormatter = RubyObjFormatter()
    processedList = rubyObjFormatter.processRubyObjList(rubyObjList)

    print("\n处理后的列表:")
    for obj in processedList:
        print(obj)