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
     
    def __init__(self, title: str, headerLen: int = 0, footerLen: int = 0, LOGGING_showRawPages: bool = False) -> None:
        self.title = title
        self.headerLen = headerLen
        self.footerLen = footerLen
        self.LOGGING_showRawPages = LOGGING_showRawPages

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

    def LOGGING_saveCharandUnicode(self, listOfParagraphs: list[str]) -> None:
        with open("char_and_uni.txt", "w") as text_file:
            for paragraph in listOfParagraphs:
                for character in paragraph:
                    line = f"{character} - {ord(character)} \n"
                    text_file.write(line)

    def _repairText(self, text: str) -> str:
        # Repairs any single pass issues
        for key in self.unicodeDict_SinglePass.keys():
                if key in text:
                    text = text.replace(key, self.unicodeDict_SinglePass[key])

        # Repais any multi pass issues
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

    def _splitParagraphs(self, text: str, headerLen: int = 0, footerLen: int = 0) -> list[str]:
        paragraphEndMarkers: list[str] = ['"', '.', '!', '?']
        textList: list = list(text)     # Convert to list for mutability
        priorCutIndex: int = 0    # Stores end of last paragraph
        breakCount: int = 0     # Counts how many line breaks the script has encountered on this page
        paragraphs: list[str] = []

        for ci in range(len(textList)): # ci - Character Index

            if ord(textList[ci]) == 10:  # If line break

                priorChar = textList[ci-1]
                breakCount += 1

                if breakCount > headerLen:  # If not in header

                    if priorChar in paragraphEndMarkers:    # If prior index seems likely for paragraph break
                        newParagraph: str = "".join(textList[priorCutIndex:ci])
                        paragraphs.append(newParagraph)
                        
                        priorCutIndex = ci

                    else:
                        textList[ci] = " "
                
                else:
                    priorCutIndex = ci
        

        lastParagraph:str = "".join(textList[priorCutIndex:])
        lastParagraph += "\n"
        paragraphs.append(lastParagraph)

        return paragraphs

    def _mendBrokenParagraphs(self) -> None:
        ...

    def pagesToParagraphList(self, pages) -> list[str]:
        processedParagraphs: list[str] = []

        for page in pages:
            rawPageText: str = str(page.get_text())
            pageText = self._repairText(text = rawPageText)  # First pass repair, this is only done to avoid possible errors

            if self.LOGGING_showRawPages:      # Prints page without paragraph logic, used to determain header/footer length 
                print(pageText)


            listOfParagraphs = self._splitParagraphs(pageText, headerLen= self.headerLen)

            for rawPar in listOfParagraphs: 
                paragraph: str = self._repairText(rawPar)   # Repeated Secondary repair pass
                processedParagraphs.append(paragraph)
        
        return processedParagraphs
            

def saveToFile(fileName: str, paragraphs: list[str]) -> None:
    with open(fileName, "w") as text_file:
        for par in paragraphs:
            text_file.write(par)

def main() -> None:
    doc = pymupdf.open("1984.pdf", filetype='.pdf') # open a document
    pdfProc = PDFProcessor(title="1984", headerLen=2)

    paragraphList: list[str] = pdfProc.pagesToParagraphList(pages= doc)
                
    pdfProc.LOGGING_saveCharandUnicode(paragraphList)
    saveToFile(fileName= "output.txt", paragraphs= paragraphList)

if __name__ == "__main__":
    main()