import re

def isMultiReFindall(patList: list[re.Pattern[str]], input: str):
    for pattern in patList:
        res = re.findall(pattern, input)
        if len(res) != 0:
            # print(pattern, input)
            return True
    return False

def execMultiReSub(patDict: dict[re.Pattern[str], str], input: str) -> str:
    res = input
    for key in patDict:
        res = re.sub(key, patDict[key], res)
    return res

def execListMultiReSub(patDict: dict[re.Pattern[str], str], input: list) -> list:
    subbedDataList: list[str] = []
    for item in input:
        subbedDataList.append(execMultiReSub(patDict, item))

    return subbedDataList