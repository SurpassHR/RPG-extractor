from typing import List
import enchant

class Formatter:
    def __init__(self) -> None:
        self.lineEnd = ['.', '?', '!', '"', "'", ')', '\\']

    def _restoreIncorrectLineBreaks(self, lines):
        restoredLines: List[str] = []
        lineCount = len(lines)

        i = 0
        while i < lineCount:
            currentLine = lines[i]
            # 检查当前行是否以换行符结尾
            isOverbound = (i >= (lineCount - 1))
            if not isOverbound and self._shouldMergeWithNextLine(currentLine, lines[i + 1]):
                # 开始构建合并行
                mergedLine = currentLine.rstrip()
                i += 1
                # 合并当前行和下一行
                while i < lineCount:
                    nextLine = lines[i]
                    if not self._shouldMergeWithNextLine(mergedLine, nextLine):
                        break
                    # 合并上下两行
                    mergedLine += ' \\n' + nextLine.strip()
                    i += 1
                restoredLines.append(mergedLine)
            else:
                # 如果当前行不需要合并，则直接添加到结果列表
                restoredLines.append(currentLine)
                i += 1

        return restoredLines

    def _shouldMergeWithNextLine(self, currentLine, nextLine):
        trimmedCurrent = currentLine.strip()
        trimmedNext = nextLine.strip()

        # 如果上下两行都是空行则不需要合并
        if not trimmedCurrent or not trimmedNext:
            return False

        # 如果句子以省略号结尾，下一行以大写字母开头，此时例外情况，需要合并
        if trimmedCurrent.endswith('...'):
            return True

        # 获取当前行最后一个字符和下一行第一个字符
        lastChar = trimmedCurrent[-1]
        firstChar = trimmedNext[0]

        # 合并条件：
        # 1. 当前行不以句子终止符结尾
        # 2. 下一行以小写字母开头
        terminated = lastChar in self.lineEnd
        return not terminated and firstChar.islower()

    def isStringValidWord(self, string: str):
        # 如果本身不是一个单词而是句子，则不能按照单词的标准判断
        if ' ' in string:
            return True
        # 如果有英文字母之外的字符，则不能按照单词的标准判断
        if not string.isalpha():
            return True
        dictionary = enchant.Dict("en_US")
        return dictionary.check(string)

    def sentenceJoint(self, strList: List[str]):
        return self._restoreIncorrectLineBreaks(strList)

if __name__ == "__main__":
    # 合并用例
    exampleLines = [
        "(I know it's just a game in which she's supposed to ",
        "be a horse, but he's being very rude.)",
        "(I guess he's the only one here who can be that ",
        "spoiled. It's just not fair.)",
        "Are you hungry?| I will make something for you to ",
        "eat right now ",
        "haha.",
        "Y- Yeah, I don't know exactly what is it about so I ",
        "can't tell how late I will be.",
        "The spore density from those mushroom creatures! ",
        "Why hadn't I thought of that?",
        "(Hah.... something...",
        "Something is coming!!)"
    ]

    correctedLines = Formatter().sentenceJoint(exampleLines)
    for line in correctedLines:
        print(line)

    word = "haha."
    print(Formatter().isStringValidWord(word))