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
    def _extractPartsandChapters(self, data) -> None:
        for text in data:
            if 'chapter' in text.lower():
                print(text)
    
    def _generateToC(self) -> str:
        chapter_file_dir: str = ''
        chapter_name: str = ''
        chapter_reference: str = f'<a href="{chapter_file_dir}">{chapter_name}</a>'

        return ''  

    def formatEpub(self, data: list[str]) -> list[str]:
        new_data: list[str] = []

        for text in data:
            new_data.append(f'<p>{text}</p>\n')
        
        return new_data

class DataOrganizer:
    def _getSectionNumber(self, section_type: str, text: str) -> str:
        section_number: str = ''

        for char in text[len(section_type):]:  # Start iterating the character following 'Chapter ' looking for int
            try:
                int(char)   # Tests if character can be converted to int
                section_number += char
            
            except ValueError:
                break

        if len(section_number) > 0: # If a chapter number was found as an int
            return section_number
            
        else:               # Start looking for a string version of the number (ie 'one', 'two')
            number_words: dict[str, int] = {
                'i': 1,
                'ii': 2,
                'iii': 3,
                'iv': 4,
                'v': 5,
                'vi': 6,
                'vii': 7,
                'viii': 8,
                'ix': 9,
                'x': 10,
                'one': 1,
                'two': 2,
                'three': 3,
                'four': 4,
                'five': 5,
                'six': 6,
                'seven': 7,
                'eight': 8,
                'nine': 9,
                'ten': 10,
                'eleven': 11,
                'twelve': 12,
                'thirteen': 13,
                'fourteen': 14,
                'fifteen': 15,
                'sixteen': 16,
                'seventeen': 17,
                'eighteen': 18,
                'nineteen': 19,
                'twenty': 20,
                'twenty-one': 21,
                'twenty-two': 22,
                'twenty-three': 23,
                'twenty-four': 24,
                'twenty-five': 25,
                'twenty-six': 26,
                'twenty-seven': 27,
                'twenty-eight': 28,
                'twenty-nine': 29,
                'thirty': 30,
                'thirty-one': 31,
                'thirty-two': 32,
                'thirty-three': 33,
                'thirty-four': 34,
                'thirty-five': 35,
                'thirty-six': 36,
                'thirty-seven': 37,
                'thirty-eight': 38,
                'thirty-nine': 39,
                'forty': 40,
                'forty-one': 41,
                'forty-two': 42,
                'forty-three': 43,
                'forty-four': 44,
                'forty-five': 45,
                'forty-six': 46,
                'forty-seven': 47,
                'forty-eight': 48,
                'forty-nine': 49,
                'fifty': 50
            }
            search_width: int = 12 # Most characters of all keys in number_words
        
        search_area: str = text[len(section_type):(len(section_type) + search_width)].lower()
        dict_keys: list = list(number_words.keys())
        dict_keys.reverse()
        for key in dict_keys:
            if key in search_area:
                return str(number_words[key])
            
        return ""

    def _getSectionMarker(self, section_type: str, data: list[str]) -> list[str]:
        new_data: list[str] = []

        if section_type[-1] != " ":
            section_type += " "

        for text in data:       
            if section_type in text:                          
                ci = text.index(section_type)   # Character Index
                section_number: str = self._getSectionNumber(section_type=section_type, text=text[ci:])

                if len(section_number) > 0:
                    section_name: str = f'{section_type}{section_number}'

                    new_data.append(text[:ci])
                    new_data.append(section_name)
                    new_data.append(text[(ci + len(section_name) + 1):])
                
                else:
                    new_data.append(text)

            else:
                new_data.append(text)
            
        return new_data
            
    def extractBookData(self, data: list[str]) -> list[str]:
        data = self._getSectionMarker(section_type='Chapter', data=data)
        data = self._getSectionMarker(section_type='Part', data=data)

        new_data: list[str] = []
        for text in data:
            if len(text) > 3:
                new_data.append(text)

        return new_data
                
class DataCleaner:
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
        "- ":       "",     # Removes word breaks between pages
        '———':      '——'
    }

    def _repairSinglePass(self, text: str) -> str:
        # Repairs any single pass issues
        for key in DataCleaner.unicode_dict_single_pass.keys():
            if key in text:
                text = text.replace(key, DataCleaner.unicode_dict_single_pass[key])
        
        return text
    
    def _repairMultiPass(self, text: str) -> str:
        # Repairs any multi pass issues
        is_errors = True

        while is_errors:
            error_list = []

            for key in DataCleaner.unicode_dict_multi_pass.keys():
                if key in text:
                    text = text.replace(key, DataCleaner.unicode_dict_multi_pass[key])
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

    data_cleaner: DataCleaner = DataCleaner()
    clean_data: list[str] = data_cleaner.cleanData(pdf_data)

    data_org: DataOrganizer = DataOrganizer()
    data: list[str] = data_org.extractBookData(clean_data)

    #form_epub: EPUBFormatter = EPUBFormatter()
    #formatted_data = form_epub.formatEpub(clean_data)

    saveToFile(file_name= "output.txt", paragraphs= data)

if __name__ == "__main__":
    main()