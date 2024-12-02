class DataOrganizer:
    def __init__(self, sections_found: list[str], data: list[str], section_names: list[str]) -> None:
        self.data: list[str] = data
        self.sections_found: list[str] = sections_found

        self.section_names: list[str] = section_names

        self.data_dict: dict = dict({})

        self.convertToDict()

    def _getSectionIndexRanges(self, unique_sections: dict[str, str]) -> dict[str, range]:
        section_indexs: dict[str, int] = dict({})

        for new_section_name in list(unique_sections.keys()):
            old_section_name: str = unique_sections[new_section_name]

            for ti in range(len(self.data)):    # Text Index
                text: str = self.data[ti]

                if old_section_name in text:
                    section_indexs[new_section_name] = ti + 1

        si = 0     # Section Idx
        section_ranges: dict[str, range] = dict({})
        sect_idx_keys: list[str] = list(section_indexs.keys())

        while si < len(sect_idx_keys) - 1:
            nsi: int = si + 1       # Next Session Idx
            
            current_section_key: str = sect_idx_keys[si]
            lower_bound: int = section_indexs[current_section_key]

            next_section_key: str = sect_idx_keys[nsi]
            upper_bound: int = section_indexs[next_section_key]

            section_ranges[current_section_key] = range(lower_bound, upper_bound)

            si += 1

        last_section_key: str = sect_idx_keys[-1]
        lower_bound = section_indexs[last_section_key]
        section_ranges[last_section_key] = range(lower_bound, len(self.data))

        return section_ranges

    def _makeSectionsUnique(self) -> dict[str, str]:
        new_dict: dict[str, str] = dict({})
        top_sect: str = self.section_names[0]
        current_prefix: str = ''

        for section in self.sections_found:
            if top_sect in section:
                current_prefix = section
                new_section_name: str = section

            else:
                new_section_name = f"{current_prefix} -:- {section}"
            
            new_dict[new_section_name] = section
        
        return new_dict

    def _divideByLowestSection(self, section_ranges: dict[str, range]) -> dict[str, list[str]]:
        data_dict: dict[str, list] = dict({})
        section_filter: str = self.section_names[-1]
        sr_keys: list = list(section_ranges.keys())

        for si in range(len(section_ranges)):
            section_key: str = sr_keys[si]

            if section_filter not in section_key:
                continue

            text_list: list[str] = []
            text_range: range = section_ranges[section_key]

            for ti in text_range:
                text: str = self.data[ti]
                text_list.append(text)
            
            data_dict[section_key] = text_list
            
        return data_dict

    def convertToDict(self) -> None:
        unique_sections: dict[str, str] = self._makeSectionsUnique()
        section_ranges: dict[str, range] = self._getSectionIndexRanges(unique_sections)
        self.data_dict = self._divideByLowestSection(section_ranges)
