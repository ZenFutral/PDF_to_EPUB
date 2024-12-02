class DataOrganizer:
    def __init__(self, section_names: list[str], data: list[str]) -> None:
        self.data: list[str] = data
        self.sections: list[str] = section_names

    def extractBookData(self) -> tuple[list[str], list[tuple[str, int]]]:
        new_data: list[str] = []
        sections_found: list[tuple[str, int]] = []

        for ti in range(len(self.data)):   # Text Index
            text: str = self.data[ti]

            if len(text) < 3:
                continue

            for si in range(len(self.section_types)): # Section Index
                type: str = self.section_types[si]
                
                if type not in text:
                    new_data.append(text)
                    continue
                
                sn_search_area: str = text[si:]
                section_number: str = self._getSectionNumber(section_name= type, text= sn_search_area)

                if section_number:
                    current_section_name = f'{type}{section_number}'
                    print(type, section_number, current_section_name)

                    new_data.append(text[si:])

                    new_data.append(current_section_name)
                    sections_found.append((current_section_name, len(new_data)))

                    following_text: str = text[len(current_section_name):]
                    new_data.append(following_text)

        sections_found = sorted(sections_found, key=lambda x: x[1])


        return (new_data, sections_found)

#    def organizeSections(self, data: list[str], sections: list[str]) -> dict:
#        book_dict: dict = {}
#        
#        for section in sections:
#            section_idx: int = data.index(section)
