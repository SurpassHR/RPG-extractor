class TranslatePostProc:
    """
    desc: 翻译相关后处理
    """

    def __init__(self):
        pass

    def init(self, rawData: dict[str, str], trData: dict[str, str]):
        """
        desc: 初始化
        rawData: dict[rawContent, rawContent]
        trData: dict[formatContent, trContent]
        """
        self._rawData: dict[str, str] = rawData
        self._trData: dict[str, str] = trData

    def procTrData(self, **kwargs) -> dict[str, str]:
        """
        **kwargs:
            sliceChar: str 分割字符，用于分割原子短语
        """
        # 构建一个新字典，内容是格式化前数据作为键，格式化前内容替换翻译作为值
        trRawData: dict = {}
        for rawKey in self._rawData.keys():
            trRawKeyMap = {
                rawKey.replace(trKey, trVal): trVal for trKey, trVal in self._trData.items() if trKey in rawKey
            }
            trRawData[rawKey] = list(trRawKeyMap.keys())[0] if len(trRawKeyMap) > 0 else rawKey

        return trRawData


class TranslateByAtomPhrase(TranslatePostProc):
    """
    desc: 根据原子短语翻译，原子短语使用指定的字符进行分割
    """

    def procTrData(self, **kwargs) -> dict[str, str]:
        sliceChar = kwargs.get("sliceChar", " ")
        # 构建一个新字典，内容是格式化前数据作为键，格式化前内容替换翻译作为值
        trRawData: dict = {}
        # 构建一个新字典，将原子短语进行分割
        trSplitData: dict = {
            sliceK: sliceV
            for trKey, trVal in self._trData.items()
            for sliceK, sliceV in zip(trKey.split(sliceChar), trVal.split(sliceChar))
            if len(trKey.split(sliceChar)) == len(trVal.split(sliceChar))
        }
        print(trSplitData)

        for rawKey in self._rawData.keys():
            trRawKeyMap = {
                rawKey.replace(trKey, trVal): trVal for trKey, trVal in trSplitData.items() if trKey in rawKey
            }
            trRawData[rawKey] = list(trRawKeyMap.keys())[0] if len(trRawKeyMap) > 0 else rawKey

        return trRawData


if __name__ == "__main__":
    rawData: dict = {
        "\\N[3] Hahahahaha": "\\N[3] Hahahahaha",
        "\\R[5] What do you think?": "\\R[5] What do you think?",
    }
    trData: dict = {
        "Hahahahaha\nWhat do you think?": "哈哈哈\n你是怎么想的？",
    }
    proc = TranslateByAtomPhrase()
    proc.init(rawData, trData)
    print(proc.procTrData(sliceChar="\n"))
