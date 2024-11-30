class PDFExtractor: 
    paragraph_end_markers: list[str] = ['"', '.', '!', '?']

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

            if prior_character in PDFExtractor.paragraph_end_markers:    # If prior index seems likely for paragraph break
                new_paragraph: str = ''.join(text_list[prior_cut_index:ci])
                prior_cut_index = ci    # Saves the end of this cut for next time
                paragraph_list.append(new_paragraph)
                    
            else:   # Replace line break with space
                text_list[ci] = " "
        
        final_paragraph: str = "".join(text_list[prior_cut_index:])
        paragraph_list.append(final_paragraph)

        paragraph_list = [p for p in paragraph_list if len(p) > 3]

        return paragraph_list

    def _extractParagraphs(self, page_data) -> list[str]:
        text_list: list = list(page_data)     # Convert to list for mutability
        list_of_paragraphs: list[str] = self._splitByLineBreaks(text_list)

        return list_of_paragraphs

    def extractData(self, pages) -> list[str]:
        data_list: list[str] = []

        for page in pages:
            raw_page_data: str = page.get_text()
            paragraphs_on_page: list[str] = self._extractParagraphs(raw_page_data)
            data_list.extend(paragraphs_on_page)
        
        return data_list 
