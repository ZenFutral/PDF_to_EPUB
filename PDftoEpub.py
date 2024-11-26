# ================================================================================================
# ================================================================================================
# AUTHOR: Zen Futral
# 
#   Many books I find free to read online are in a pdf format. I use Google Books to read, which 
# performs best when working with an '.epub' file, by this I mean, the app provides more viewing
# customability. 
# ================================================================================================
# ================================================================================================

import pymupdf #type: ignore
from time import sleep
       
class PDFProcessor:
    
    def __init__(self, title: str, headerLen: int = 0, footerLen: int = 0, showRawPages: bool = False) -> None:
        self.title = title
        self.headerLen = headerLen
        self.footerLen = footerLen
        self.showRawPages = showRawPages

        self.unicodeDict_SinglePass: dict[str, str] = {
            '\u037e':   "",     # Greek Questionmark
            '\uf645':   "",     # PUA: Private Use Area
            '\uf646':   "",     # PUA
            '\uf648':   "",     # PUA
            '\uf649':   "",     # PUA
            '\uf64a':   "",     # PUA
            chr(39):    "'",    # Single Quote
            chr(160):   " ",    # Non-Breaking Space
            chr(173):   "-",    # Inverted Exclamation Mark
            chr(8212):  "--",   # Em Dash
            chr(8217):  '"',    # Right Single Quotation Mark
            chr(8216):  '"',    # Left Single Quotation Mark
            chr(8221):  '"',     # Right Double Quotation Mark
            chr(8220):  '"'     # Left Double Quotation Mark
        }

        self.unicodeDict_MultiPass: dict[str, str] = {
            "  ":       " ",    # Fixes double space
            "- ":       ""  
        }

    def repairText(self, text: str) -> str:
        for key in self.unicodeDict_SinglePass.keys():
                if key in text:
                    text = text.replace(key, self.unicodeDict_SinglePass[key])

        isErrors = True

        while isErrors:
            errorList = []
            for key in self.unicodeDict_MultiPass.keys():
                if key in text:
                    text = text.replace(key, self.unicodeDict_MultiPass[key])
                    errorList.append(True)
                
                else:
                    errorList.append(False)
        
            if True not in errorList:
                isErrors = False

        return text

    def splitParagraphs(self, text: str, headerLen: int = 0, footerLen: int = 0) -> list[str]:
        paragraphEndMarkers: list[str] = ['"', '.', '!', '?']
        textList: list = list(text) # Convert to list for mutability
        lastCut: int = 0
        breakCount: int = 0 # Counts how many line breaks the script has encountered on this page
        paragraphs: list[str] = []

        for i in range(len(textList)):

            if ord(textList[i]) == 10:  # If line break

                priorChar = textList[i-1]
                breakCount += 1

                if breakCount > headerLen:
                    if priorChar in paragraphEndMarkers:    # If prior index seems likely for paragraph break
                        newParagraph:str = "".join(textList[lastCut:i])
                        newParagraph += '\n'
                        paragraphs.append(newParagraph)
                        
                        lastCut = i

                    else:   # If prior index doesn't seem like paragraph end, replace with space
                        textList[i] = " "
                
                else:
                    lastCut = i
        

        lastParagraph:str = "".join(textList[lastCut:])
        lastParagraph += "\n"
        paragraphs.append(lastParagraph)

        return paragraphs

    def mendBrokenParagraphs(self) -> None:
        ...

    def printCharandUnicode(self, pages: list[list[str]]) -> None:
        with open("char_and_uni.txt", "w") as text_file:
            for listOfParagraphs in pages:
                for paragraph in listOfParagraphs:
                    for character in paragraph:
                        line = f"{character} - {ord(character)} \n"
                        text_file.write(line)

    def getPageText(self, page) -> list[str]:
        rawPageText: str = str(page.get_text())
        pageText = self.repairText(text = rawPageText)

        if self.showRawPages:
            print(pageText)

        listOfParagraphs = self.splitParagraphs(str(pageText), headerLen=self.headerLen)
        processedPar = []

        for rawPar in listOfParagraphs:
            processedPar.append(self.repairText(rawPar))
        
        return(processedPar)

def saveToFile(fileName: str, pages: list[list[str]]) -> None:
    with open(fileName, "w") as text_file:
        for page in pages:
            for paragraph in page:
                text_file.write(paragraph)

def main() -> None:
    doc = pymupdf.open("1984.pdf", filetype='.pdf', ) # open a document
    pdfProc = PDFProcessor(title="1984", headerLen=2)

    processedPages: list[list[str]] = []
    pageNumber = 0

    for rawPage in doc: # iterate the document pages
        pageNumber += 1
        processedPages.append(pdfProc.getPageText(rawPage))
        
        print(f"Page Finished: {pageNumber} / {len(doc)}")
        print("===============")
        print("")
        
    # printCharandUnicode(processedPages)
    saveToFile(fileName= "output.txt", pages= processedPages)

if __name__ == "__main__":
    main()