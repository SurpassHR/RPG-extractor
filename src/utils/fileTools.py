import os
import json
import shutil
import threading


def readJson(filePath: str) -> dict:
    """
    desc: 读取 json 文件为 dict
    params:
        filePath: json 文件路径
    returns: json 内容，若读取失败返回空字典
    """
    try:
        with open(filePath, "r", encoding="utf-8") as jsonFile:
            jsonContent = json.load(jsonFile)
        return jsonContent
    except Exception as _:
        return {}


def isFolder(path: str) -> bool:
    return os.path.isdir(path)


def copyFolder(path: str, newPath: str) -> None:
    """
    desc: 复制文件夹
    params:
        path: 源文件夹路径
        newPath: 目标文件夹路径
    """
    shutil.copytree(path, newPath)


def isFile(path: str) -> bool:
    return os.path.isfile(path)


def getFileName(path: str) -> str:
    return os.path.basename(path)


def getFileNameWithoutExt(path) -> str:
    return getFileName(path).split(".")[0]


def getFileExt(path: str) -> str:
    return os.path.splitext(path)[1].replace(".", "")


def getFileParentFolder(path: str) -> str:
    return os.path.split(os.path.dirname(path))[-1]


def isPathExists(path: str) -> bool:
    return os.path.exists(path)


def isFolderExists(path: str) -> bool:
    return os.path.isdir(path) and os.path.exists(path)


def isFileExists(path: str) -> bool:
    return os.path.isfile(path) and os.path.exists(path)


def getBufferedReader(path: str, bufferSize: int = 1024) -> object:
    if not isFileExists(path):
        return None
    return open(path, "rb", buffering=bufferSize)


def isFileInListValid(fileList: list[str]) -> bool:
    if fileList is None or len(fileList) == 0:
        return False

    for filePath in fileList:
        if not isFileExists(filePath):
            return False
    return True


def getAllFilesFromFolder(folderPath: str) -> list[str]:
    """
    desc: 获取文件夹下的所有文件
    params:
        folderPath: 文件夹路径
    returns: list 文件夹下的所有文件的绝对路径
    """
    if not isFolderExists(folderPath):
        return []

    fileList = os.listdir(folderPath)
    fileList = [os.path.abspath(os.path.join(folderPath, file)) for file in fileList]

    return fileList


def getFilesInFolderByType(folderPath: str, fileExt: str) -> list[str]:
    """
    desc: 获取文件夹下的给出文件类型的所有文件
    params:
        folderPath: 文件夹路径
    returns: list 文件夹下的给出文件类型的所有文件的绝对路径
    """
    fileList = getAllFilesFromFolder(folderPath)
    fileList = [file for file in fileList if isFile(file) and getFileExt(file) == fileExt]
    fileList = [os.path.abspath(os.path.join(folderPath, file)) for file in fileList]

    return fileList


def getFilesInFolderByTypes(folderPath: str, fileExts: list[str]) -> list[str]:
    ret: list[str] = []
    for ext in fileExts:
        ret.extend(getFilesInFolderByType(folderPath, ext))

    return ret


list_file_lock = threading.Lock()


def dumpListToFile(dataList: list, fileName: str, firstWrite: bool = True) -> None:
    with list_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
        if dataList is not None and dataList != []:
            with open(fileName, "a", encoding="utf-8") as f:
                dataList = [item for item in dataList if item != ""]
                json.dump(dataList, f, ensure_ascii=False, indent=4)


def writeListToFile(dataList: list, fileName: str, firstWrite: bool = True) -> None:
    with list_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
        if dataList is not None and dataList != []:
            with open(fileName, "a", encoding="utf-8") as f:
                for item in dataList:
                    f.write(str(item) + "\n")


dict_file_lock = threading.Lock()


def writeDictToJsonFile(dataDict: dict, fileName: str, firstWrite: bool = True) -> None:
    with dict_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
    if dataDict is not None and dataDict != {}:
        with open(fileName, "a", encoding="utf-8") as f:
            json.dump(dataDict, f, ensure_ascii=False, indent=4)
            f.write("\n")


ruby_file_lock = threading.Lock()


def writeListToRubyFile(dataList: list, fileName: str, firstWrite: bool = True) -> None:
    with ruby_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
    with open(fileName, "a", encoding="utf-8") as rbFile:
        for item in dataList:
            if not item:
                continue
            rbFile.write("{}".format(item.replace("\r", "")))


class FileTool:
    def __init__(self) -> None:
        pass

    def _exportListToJson(self, data: list, exportJson: str) -> None:
        jsonContent: dict = {}
        for item in data:
            key = val = f"{item}"
            jsonContent[key] = val

        writeDictToJsonFile(jsonContent, exportJson, True)
