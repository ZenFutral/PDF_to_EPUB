class DataOrganizer:
    def __init__(self, section_names: list[str]) -> None:
        self.section_names: list[str] = section_names

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

    def _fixDropcapSpace(self, text: str) -> str:
        first_char: str = text[0]
        one_char_words: list[str] = ['a', 'i']

        if first_char.lower() not in one_char_words:
            print(f'{first_char}{text[2:]}')
            return f'{first_char}{text[2:]}'
        
        else:
            return text

    def _getSectionMarker(self, section_type: str, sections_found: list[tuple[str, int]], data: list[str]):
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
                    sections_found.append((section_name, len(new_data)))

                    following_text: str = text[(ci + len(section_name)):]
                    new_data.append(following_text)
                
                else:
                    new_data.append(text)

            else:
                new_data.append(text)

        new_data = [self._fixDropcapSpace(text) for text in new_data]
        return new_data, sections_found
            
    def extractBookData(self, data: list[str]) -> tuple[list[str], list[str]]:
        sections_found: list[tuple[str, int]] = []  #Tuple is (Section Name, Line) Example: [(Part 1, 1), (Chapter 1, 2), (Chapter 2, 20)]

        for name in self.section_names:
            data, sections_found = self._getSectionMarker(sections_found=sections_found, section_type=name, data=data)
        
        sections_found = sorted(sections_found, key=lambda x: x[1])
        sections: list[str] = [section[0] for section in sections_found]    # Strips line index, since that will be meaningless after the following line where empty strings are dismissed.

        new_data: list[str] = [text for text in data if len(text) > 3]

        return (new_data, sections)

#    def organizeSections(self, data: list[str], sections: list[str]) -> dict:
#        book_dict: dict = {}
#        
#        for section in sections:
#            section_idx: int = data.index(section)
