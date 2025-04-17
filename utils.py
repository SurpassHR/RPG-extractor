import os
import threading
from rubymarshal.classes import RubyString
from definitions import FileType
from typing import List

PRINT_LIST_FLG = False
def printList(dataList: list, needPrint: bool) -> None:
    if not PRINT_LIST_FLG and not needPrint:
        return
    if dataList is not None and dataList != []:
        for item in dataList:
            print(item)

LIST_WRITE_FILE_FLG = True
file_lock = threading.Lock()
def writeListToFile(dataList: list, fileName: str, firstWrite: bool) -> None:
    if not LIST_WRITE_FILE_FLG:
        return

    with file_lock:
        if firstWrite and os.path.exists(fileName):
            os.remove(fileName)
        if dataList is not None and dataList != []:
            with open(fileName, 'a') as f:
                for item in dataList:
                    f.write(str(item) + '\n')

def traverseListBytesDecode(dataList: list) -> list:
    retList = []
    for item in dataList:
        if isinstance(item, list):
            retList.extend(traverseListBytesDecode(item))
            continue
        if isinstance(item, str):
            retList.append(item)
            continue
        if isinstance(item, RubyString):
            retList.append(item.text)
            continue
        if isinstance(item, bytes):
            item = item.decode('utf-8')
            retList.append(item)
            continue

    return retList

def getFileListFromPath(extractPath: str, fileType: FileType) -> list:
    fileExt = fileType.value
    fileList = os.listdir(extractPath)
    fileList = [file for file in fileList if os.path.splitext(file)[1] == fileExt]
    fileList = [os.path.join(extractPath, file) for file in fileList]

    return fileList

def listDedup(dataList: list) -> list:
    tempDataList = []
    [tempDataList.append(item) for item in dataList if item not in tempDataList]
    return tempDataList

def hashableListDedup(dataList: list) -> list:
    return list(dict.fromkeys(dataList))

def nonSeqListDedup(dataList: list) -> list:
    return list(set(dataList))

def sentenceJoint(strList: List[str]):
    def restoreIncorrectLineBreaks(lines):
        """
        Restores sentences that were incorrectly split across multiple lines.
        Enhanced to handle cases like mid-sentence uppercase words after ellipses.
        """
        restoredLines = []
        i = 0
        lineCount = len(lines)

        while i < lineCount:
            currentLine = lines[i]

            # Check if we should start merging lines
            if i < lineCount - 1 and (currentLine.rstrip() != currentLine or
                                    shouldMergeWithNextLine(currentLine, lines[i + 1])):

                # Start building the merged line
                mergedLine = currentLine.rstrip()
                i += 1

                # Keep merging subsequent lines while the conditions are met
                while i < lineCount:
                    nextLine = lines[i]
                    trimmedNext = nextLine.strip()

                    # Special case: Allow uppercase if previous line ends with ellipsis
                    allowUppercase = mergedLine.rstrip().endswith('...')

                    # Stop merging if:
                    # 1. Next line is empty
                    # 2. Next line starts with uppercase (unless after ellipsis)
                    # 3. Current merged line ends with sentence terminator
                    if (not trimmedNext or
                        (trimmedNext and trimmedNext[0].isupper() and not allowUppercase) or
                        (mergedLine.rstrip().endswith(('.', '?', '!', '"', "'", ')', '\\')) and not mergedLine.rstrip().endswith('...'))):
                        break

                    # Add to merged line (with single space)
                    mergedLine += ' ' + trimmedNext
                    i += 1

                restoredLines.append(mergedLine)
            else:
                # No merge needed, add current line as is
                restoredLines.append(currentLine)
                i += 1

        return restoredLines

    def shouldMergeWithNextLine(currentLine, nextLine):
        """Helper function to determine if two lines should be merged"""
        trimmedCurrent = currentLine.strip()
        trimmedNext = nextLine.strip()

        # Don't merge if either line is empty
        if not trimmedCurrent or not trimmedNext:
            return False

        lastChar = trimmedCurrent[-1]
        firstChar = trimmedNext[0]

        # Special case: Allow uppercase if line ends with ellipsis
        if trimmedCurrent.endswith('...'):
            return True

        # Conditions for merging:
        # 1. Current doesn't end with sentence terminator
        # 2. Next line starts with lowercase letter
        return (lastChar not in {'.', '?', '!', '"', "'", ')', '\\'} and
                firstChar.islower())

    return restoreIncorrectLineBreaks(strList)

if __name__ == "__main__":
    exampleLines = [
        "(I know it's just a game in which she's supposed to ",  # Note trailing space
        "be a horse, but he's being very rude.)",
        "(I guess he's the only one here who can be that ",  # Trailing space
        "spoiled. It's just not fair.)",
        "Are you hungry?| I will make something for you to ",  # Trailing space
        "eat right now ",
        "haha.",
        "Y- Yeah, I don't know exactly what is it about so I ",  # Trailing space
        "can't tell how late I will be.",
        "The spore density from those mushroom creatures! ",
        "Why hadn't I thought of that?",
        "(Hah.... something...",
        "Something is coming!!)"
    ]

    correctedLines = sentenceJoint(exampleLines)
    for line in correctedLines:
        print(line)