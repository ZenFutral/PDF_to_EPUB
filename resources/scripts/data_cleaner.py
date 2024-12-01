class DataCleaner:
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

    def __init__(self, sections: list[str]) -> None:
        self.sections: list[str] = sections

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
            print(i, len(data))
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


            elif last_char not in DataCleaner.paragraph_end_markers:
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
