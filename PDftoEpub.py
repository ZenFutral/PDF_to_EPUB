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
       
class pdf_processor: 
    def __init__(self, title: str, header_len: int = 0, footer_len: int = 0, LOGGING_show_raw_pages: bool = False) -> None:
        self.title = title
        self.header_len = header_len
        self.footer_len = footer_len
        self.LOGGING_show_raw_pages = LOGGING_show_raw_pages

        self.unicode_dict_single_pass: dict[str, str] = {
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

        self.unicode_dict_multi_pass: dict[str, str] = {
            #chr(10):    "test",
            "  ":       " ",    # Fixes double space
            "- ":       "-"  
        }

        self.paragraph_end_markers: list[str] = ['"', '.', '!', '?']

    def LOGGING_saveCharandUnicode(self, list_of_paragraphs: list[str]) -> None:
        with open("char_and_uni.txt", "w") as text_file:
            for paragraph in list_of_paragraphs:
                for character in paragraph:
                    line = f"{character} - {ord(character)} \n"
                    text_file.write(line)

    def _repairText(self, text: str) -> str:
        # Repairs any single pass issues
        for key in self.unicode_dict_single_pass.keys():
            if key in text:
                text = text.replace(key, self.unicode_dict_single_pass[key])

        # Repairs any multi pass issues
        is_errors = True

        while is_errors:
            error_list = []

            for key in self.unicode_dict_multi_pass.keys():
                if key in text:
                    text = text.replace(key, self.unicode_dict_multi_pass[key])
                    error_list.append(True)
                
                else:
                    error_list.append(False)
        
            if True not in error_list:   # If not errors logged in this cycle
                is_errors = False

        return text

    def _stripExtraChars(self, text: str) -> str:
        characters_to_strip: list[str] = ['\n', ' ']

        for c in characters_to_strip:
            text = text.strip(c)
        
        text = text.replace('\n', '')   # Found that some random line breaks were getting through prior cleanings
        return text

    def _splitPagetoLines(self, text: str, header_len: int = 0, footer_len: int = 0) -> list[str]:
        text_list: list = list(text)     # Convert to list for mutability
        prior_cut_index: int = 0    # Stores end of last paragraph
        break_count: int = 0     # Counts how many line breaks the script has encountered on this page
        paragraphs: list[str] = []

        for ci in range(len(text_list)): # ci - Character Index
            if ord(text_list[ci]) == 10:  # If line break
                prior_character = text_list[ci-1]
                break_count += 1     # Tracks line breaks to estimate line number
                
                if break_count < header_len:  # If still in header lines
                    prior_cut_index = ci
                    continue
                
                if prior_character in self.paragraph_end_markers:    # If prior index seems likely for paragraph break
                    new_paragraph: str = ''
                    new_paragraph = "".join(text_list[prior_cut_index:ci])
                    prior_cut_index = ci
                    paragraphs.append(new_paragraph)
                    
                else:
                    text_list[ci] = " "
        
        final_paragraph:str = "".join(text_list[prior_cut_index:])
        paragraphs.append(final_paragraph)

        stripped_paragraphs: list[str] = [self._stripExtraChars(p) for p in paragraphs]

        return stripped_paragraphs

    def _notEmptyParagraph(self, text: str) -> bool:
        return not all(c == chr(10) for c in text)

    def _mendSplitParagraphs(self, paragraphs: list[str]) -> list[str]:
        new_paragraph_list: list[str] = []
        skip_paragraph: bool = False

        for pi in range(len(paragraphs)):  #pi - Paragraph Index
            if skip_paragraph:
                skip_paragraph = False
                continue

            par: str = paragraphs[pi]

            if (par[-1] == '-') or (par[-1] not in self.paragraph_end_markers):   # If line ends in a broken word, or ends abruptly
                try:
                    next_paragraph: str = paragraphs[pi + 1]
                    new_paragraph_list.append(par[:-2] + next_paragraph)
                    
                    skip_paragraph = True # Skips the next paragraph, since we attatched it to the current one

                except IndexError:
                    new_paragraph_list.append(par)

            else:
                new_paragraph_list.append(par)

        return new_paragraph_list

    def pagesToparagraph_list(self, pages) -> list[str]:
        processed_paragraphs: list[str] = []

        for page in pages:
            raw_page_text: str = str(page.get_text())
            page_text = self._repairText(text = raw_page_text)  # First pass repair, this is only done to avoid possible errors

            if self.LOGGING_show_raw_pages:      # Prints page without paragraph logic, used to determain header/footer length 
                print(page_text)

            list_of_paragraphs: list[str] = self._splitPagetoLines(page_text, header_len = self.header_len)

            # Repeated Secondary repair pass & Removes empty paragraphs
            for paragraph in list_of_paragraphs:
                if self._notEmptyParagraph(paragraph):
                    processed_paragraphs.append(self._repairText(paragraph))
        
        # Mends weird breaks where there shouldn't be
        processed_paragraphs = self._mendSplitParagraphs(processed_paragraphs)

        return processed_paragraphs 

class FormatToEpub:
    def __init__(self, paragraph_list: list[str]) -> None:
        self.paragraph_list = paragraph_list
    
    def _extractPartsandChapters(self) -> None:
        for p in self.paragraph_list:
            if 'chapter' in p.lower():
                print(p)
    
    def _generateToC(self) -> str:
        chapter_file_dir: str = ''
        chapter_name: str = ''
        chapter_reference: str = f'<a href="{chapter_file_dir}">{chapter_name}</a>'

        return ''  

    def formatEpub(self) -> list[str]:
        new_paragraphs: list[str] = []

        for par in self.paragraph_list:
            new_paragraphs.append(f'<p>{par}</p>\n')
        
        return new_paragraphs

def saveToFile(file_name: str, paragraphs: list[str]) -> None:
    with open(file_name, "w") as text_file:
        for par in paragraphs:
            text_file.write(par)

def main() -> None:
    file_name: str = '1984.pdf'
    doc = pymupdf.open(file_name, filetype='.pdf') # open a document

    pdf_proc = pdf_processor(title="1984", header_len=2)
    paragraph_list: list[str] = pdf_proc.pagesToparagraph_list(pages= doc)

    form_epub = FormatToEpub(paragraph_list= paragraph_list)
    paragraph_list = form_epub.formatEpub()
    form_epub._extractPartsandChapters()

    pdf_proc.LOGGING_saveCharandUnicode(paragraph_list)
    saveToFile(file_name= "output.txt", paragraphs= paragraph_list)

if __name__ == "__main__":
    main()