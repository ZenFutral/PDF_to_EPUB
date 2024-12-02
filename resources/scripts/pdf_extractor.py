from time import sleep

class PDFExtractor: 
    paragraph_end_markers: list[str] = ['"', '.', '!', '?']

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

    number_dict: dict[str, int] = {
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

    def __init__(
            self, 
            pages,
            section_types: list[str],
            title_pages_len: int = 0, 
            header_len: int = 0, 
            footer_len: int = 0, 
            LOGGING_show_raw_pages: bool = False

        ) -> None:
        
        # Class init arguments
        self.pages = pages
        self.section_types = section_types
        self.title_pages_len = title_pages_len - 1
        self.header_len = header_len
        self.footer_len = footer_len
        self.LOGGING_show_raw_pages = LOGGING_show_raw_pages

        # Class init empty variables
        self.sections_found: list[str] = []
        self.new_data: list[str] = []

        # Run logic
        self.extractData()
        self.cleanData()

    def LOGGING_saveCharandUnicode(self, list_of_paragraphs: list[str]) -> None:
        with open("char_and_uni.txt", "w") as text_file:
            for paragraph in list_of_paragraphs:
                for character in paragraph:
                    line = f"{character} - {ord(character)} \n"
                    text_file.write(line)

    def _cutByEndMarkers(self, text_list: list[str]) -> list[str]:
        prior_cut_index: int = 0    # Stores end of last paragraph
        break_count: int = 0     # Counts how many line breaks the script has encountered on this page
        data: list[str] = []

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

            if prior_character in PDFExtractor.paragraph_end_markers:    # If prior index seems likely for paragraph break
                new_paragraph: str = ''.join(text_list[prior_cut_index:ci])
                prior_cut_index = ci    # Saves the end of this cut for next time
                data.append(new_paragraph)
                    
            else:   # Replace line break with space
                text_list[ci] = " "
        
        final_paragraph: str = "".join(text_list[prior_cut_index:])
        data.append(final_paragraph)

        return data

    def _cutBySection(self, text_list: list[str]) -> list[str]:
        data: list[str] = []
        for text in text_list:
            section_fragment: list[str] = self._findSectionHeader(text)

            if section_fragment:
                data.extend(section_fragment)
            
            else:
                data.append(text)
        
        return data

    def _searchForInts(self, text: str) -> str:
        section_number: str = ''
        for char in text:  # Start iterating the character following 'Chapter ' looking for int
            if char == " ":
                continue

            if char.isnumeric():
                section_number += char
        
        return section_number
    
    def _searchForStrs(self, text: str):
        dict_keys: list = list(PDFExtractor.number_dict.keys())
        dict_keys.reverse()

        for key in dict_keys:
            if key in text:
                return str(PDFExtractor.number_dict[key])
            
        return ""

    def _getSectionNumber(self, section_type: str, text: str) -> str:
        len_section_type: int = len(section_type)

        # Start looking for a string version of the number (ie 'one', 'two')
        search_width: int = 12 + len_section_type + 2   # Most characters of all keys in number_dict
        search_text: str = text[:search_width].lower()

        section_number: str = self._searchForInts(text = search_text)

        if not section_number:
            section_number = self._searchForStrs(text = search_text)
        
        return section_number
        
    def _fixDropcapSpace(self, text: str) -> str:
        first_char: str = text[0]
        one_char_words: list[str] = ['a', 'i']
        return_text: str = ''

        if first_char.lower() not in one_char_words:
            si: int = text.index(" ")
            return_text = f'{first_char}{text[si + 1:]}'

        
        return return_text

    def _findSectionHeader(self, text: str) -> list[str]:
        section_number: str = ''

        for type in self.section_types:
            if type[-1] != " ":
                type = type + " "

            if type in text:
                section_number = self._getSectionNumber(section_type= type, text= text)
                hi: int = text.index(type) # Header Index
                break
            
        if len(section_number) < 1:
            return []

        pre_text: str = text[:hi] + '\n'

        header_name: str = f"{type}{section_number}"
        self.sections_found.append(header_name) 

        header_buffer: int = len(header_name) + hi
        post_text: str = text[header_buffer:].strip()
        
        if post_text[0].islower():
            post_text = ''

        else:
            post_text = self._fixDropcapSpace(text= post_text)
        

        section_fragment: list[str] = [pre_text, header_name, post_text]   
        return section_fragment

    def _splitByLineBreaks(self, text_list: list[str]) -> list[str]:
        paragraph_list: list[str] = self._cutByEndMarkers(text_list)

        paragraph_list = self._cutBySection(text_list= paragraph_list)
        
        data = [p for p in paragraph_list if len(p) > 3]

        return data

    def _extractParagraphs(self, page_data) -> list[str]:
        text_list: list = list(page_data)     # Convert to list for mutability
        list_of_paragraphs: list[str] = self._splitByLineBreaks(text_list)

        return list_of_paragraphs

    def extractData(self) -> None:
        for pi in range(len(self.pages)): # Page Index
            page = self.pages[pi]

            if pi <= self.title_pages_len:
                continue

            raw_page_data: str = page.get_text()
            paragraphs_on_page: list[str] = self._extractParagraphs(raw_page_data)
            self.new_data.extend(paragraphs_on_page)
        
# =========================================================================

    def _repairSinglePass(self, text: str) -> str:
        # Repairs any single pass issues
        for key in PDFExtractor.unicode_dict_single_pass.keys():
            if key in text:
                text = text.replace(key, PDFExtractor.unicode_dict_single_pass[key])
        
        return text
    
    def _repairMultiPass(self, text: str) -> str:
        # Repairs any multi pass issues
        is_errors = True

        while is_errors:
            error_list = []

            for key in PDFExtractor.unicode_dict_multi_pass.keys():
                if key in text:
                    text = text.replace(key, PDFExtractor.unicode_dict_multi_pass[key])
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
    
    def _lastIdxIsInt(self, char: str) -> bool:
        if char.isnumeric():
            return True
        
        else:
            return False
        
    def _repairBadBreaks(self, data: list[str]) -> tuple[list[str], bool]:
        repaired_something: bool = False
        skip_paragraph: bool = False
        new_data_list: list[str] = []

        for i in range(len(data)):
            if i == (len(data) - 1):    # If last line
                break

            if skip_paragraph:
                skip_paragraph = False
                continue

            current_paragraph: str = data[i]    # If empty paragraph
            if len(current_paragraph) < 1:
                continue

                    
            last_char: str = current_paragraph[-1]            

            if self._lastIdxIsInt(last_char):
                new_paragraph: str = '\n' + current_paragraph
                new_data_list.append(new_paragraph)
                continue


            elif last_char not in PDFExtractor.paragraph_end_markers:
                repaired_something = True
                skip_paragraph = True
                next_paragraph: str = data[i + 1]
                new_paragraph = current_paragraph + next_paragraph
                new_data_list.append(new_paragraph)
                continue
            
            repaired_something = False
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

            if len(checker_text) < 3:
                continue

            else:
                new_data.append(text)
            
        return new_data

    def cleanData(self) -> None:
        data = self.new_data

        data = [self._repairText(text) for text in data]
        data = [text.strip() for text in data]
        data = self._initiateBadBreakRepair(data)
        data = self._removeEmptyLines(data)
        
        self.new_data = data
