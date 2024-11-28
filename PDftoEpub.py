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

paragraph_end_markers: list[str] = ['"', '.', '!', '?']


class EPUBFormatter:
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

class DataProcessor:
    unicode_dict_single_pass: dict[str, str] = {
        # PUA: Private Use Area
        '\uf645':               "",                 
        '\uf646':               "",                 
        '\uf647':               "",                 
        '\uf648':               "",                 
        '\uf649':               "",                 
        '\uf64a':               "",   
        # =====================
        # Formatting Choices              
        f" {chr(8216)}":       f" {chr(8220)}",     # Left  Single Quotation Mark, preceeded by space
        f"\n{chr(8216)}":      f"\n{chr(8220)}",    # Left  Single Quotation Mark, preceeded by break
        chr(8216):              "'",                # Left  Single Quotation Mark
        f".{chr(8217)}":       f".{chr(8221)}",     # Right Single Quotation Mark, preceeded by .
        f",{chr(8217)}":       f",{chr(8221)}",     # Right Single Quotation Mark, preceeded by ,
        f"!{chr(8217)}":       f"!{chr(8221)}",     # Right Single Quotation Mark, preceeded by !
        f"?{chr(8217)}":       f"?{chr(8221)}",     # Right Single Quotation Mark, preceeded by ?
        f"—{chr(8217)}":       f"—{chr(8221)}",     # Right Single Quotation Mark, preceeded by —

        chr(8217):              "'",                # Right Single Quotation Mark

        '— —' : '——',
        '\n': ''
    }

    unicode_dict_multi_pass: dict[str, str] = {
        "  ":       " ",    # Fixes double space
        "- ":       ""      # Removes word breaks between pages
    }

    def _repairSinglePass(self, text: str) -> str:
        # Repairs any single pass issues
        for key in DataProcessor.unicode_dict_single_pass.keys():
            if key in text:
                text = text.replace(key, DataProcessor.unicode_dict_single_pass[key])
        
        return text
    
    def _repairMultiPass(self, text: str) -> str:
        # Repairs any multi pass issues
        is_errors = True

        while is_errors:
            error_list = []

            for key in DataProcessor.unicode_dict_multi_pass.keys():
                if key in text:
                    text = text.replace(key, DataProcessor.unicode_dict_multi_pass[key])
                    error_list.append(True)
                
                else:
                    error_list.append(False)
        
            if True not in error_list:   # If not errors logged in this cycle
                is_errors = False

        return text

    def _repairText(self, text: str) -> str:
        text = self._repairSinglePass(text)
        text = self._repairMultiPass(text)

        return text

    def _repairBadBreaks(self, data: list[str]) -> tuple[list[str], bool]:
        repaired_something: bool = False
        new_data_list: list[str] = []
        skip_paragraph: bool = False

        for i in range(len(data)):
            if skip_paragraph:
                skip_paragraph = False
                continue

            if i == (len(data) - 1):
                break

            current_paragraph: str = data[i]
            last_char: str = current_paragraph[-1]
            if last_char not in paragraph_end_markers:
                repaired_something = True
                next_paragraph: str = data[i + 1]
                new_paragraph: str = current_paragraph + next_paragraph
                skip_paragraph = True
            
            else:
                new_paragraph = current_paragraph

            new_data_list.append(new_paragraph)
        
        return new_data_list, repaired_something

    def _initiateBadBreakRepair(self, data: list[str]) -> list[str]:
        repairing: bool = True

        while repairing:
            data, repairing = self._repairBadBreaks(data)

        return data

    def _removeEmptyLines(self, data: list[str]) -> list[str]:
        new_data: list[str] = []

        for text in data:
            checker_text: str = text.replace('\n', '').replace(' ', '')
            if len(checker_text) == 0:
                continue

            else:
                new_data.append(text)
            
        return new_data

    def cleanData(self, data: list[str]) -> list[str]:
        data = [self._repairText(text) for text in data]
        data = [text.strip() for text in data]
        data = self._removeEmptyLines(data)
        data = self._initiateBadBreakRepair(data)

        return data

class PDFExtractor: 
    def __init__(self, title: str, header_len: int = 0, footer_len: int = 0, LOGGING_show_raw_pages: bool = False) -> None:
        self.title = title
        self.header_len = header_len
        self.footer_len = footer_len
        self.LOGGING_show_raw_pages = LOGGING_show_raw_pages


    def LOGGING_saveCharandUnicode(self, list_of_paragraphs: list[str]) -> None:
        with open("char_and_uni.txt", "w") as text_file:
            for paragraph in list_of_paragraphs:
                for character in paragraph:
                    line = f"{character} - {ord(character)} \n"
                    text_file.write(line)

    def _splitByLineBreaks(self, text_list: list[str]) -> list[str]:
        paragraph_list: list[str] = []
        prior_cut_index: int = 0    # Stores end of last paragraph
        break_count: int = 0     # Counts how many line breaks the script has encountered on this page

        for ci in range(len(text_list)): # ci - Character Index
            current_unicode: int = ord(text_list[ci])
            prior_character: str = ''

            if current_unicode == 10:  # If line break
                prior_character = text_list[ci-1]
                break_count += 1     # Tracks line breaks to estimate line number
            
            else:   # If not line break, just skip
                continue

            if break_count <= self.header_len:  # If still in header lines
                prior_cut_index = ci
                continue

            if prior_character in paragraph_end_markers:    # If prior index seems likely for paragraph break
                new_paragraph: str = ''.join(text_list[prior_cut_index:ci])
                prior_cut_index = ci    # Saves the end of this cut for next time
                paragraph_list.append(new_paragraph)
                    
            else:   # Replace line break with space
                text_list[ci] = " "
        
        final_paragraph: str = "".join(text_list[prior_cut_index:])
        paragraph_list.append(final_paragraph)

        return paragraph_list

    def _extractParagraphs(self, page_data) -> list[str]:
        text_list: list = list(page_data)     # Convert to list for mutability
        list_of_paragraphs: list[str] = self._splitByLineBreaks(text_list)

        return list_of_paragraphs

    def extractData(self, pages) -> list[str]:
        master_list_of_strings: list[str] = []

        for page in pages:
            raw_page_data: str = page.get_text()
            paragraphs_on_page: list[str] = self._extractParagraphs(raw_page_data)
            master_list_of_strings.extend(paragraphs_on_page)
        
        return master_list_of_strings 

def saveToFile(file_name: str, paragraphs: list[str]) -> None:
    with open(file_name, "w", encoding='utf-16') as text_file:
        for par in paragraphs:
            text_file.write(par + '\n')
    
    with open((file_name + '_repr'), "w", encoding='utf-16') as text_file:
        for par in paragraphs:
            text_file.write(repr(par + '\n'))


def main() -> None:
    file_name: str = '1984.pdf'
    document = pymupdf.open(file_name, filetype = '.pdf',)

    pdf_extractor: PDFExtractor = PDFExtractor(title = "1984", header_len = 2)
    pdf_data: list[str] = pdf_extractor.extractData(pages = document)

    data_processor: DataProcessor = DataProcessor()
    clean_data: list[str] = data_processor.cleanData(pdf_data)


    saveToFile(file_name= "output.txt", paragraphs= clean_data)
    '''
    form_epub = FormatToEpub(paragraph_list= paragraph_list)
    paragraph_list = form_epub.formatEpub()
    #form_epub._extractPartsandChapters()

    pdf_processor.LOGGING_saveCharandUnicode(paragraph_list)
    '''

if __name__ == "__main__":
    main()