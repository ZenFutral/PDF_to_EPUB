class EPUBExport:
    html_tail: str = '''
        </body>
        </html>
    '''

    save_counter: int = 0

    def __init__(self, data_dict: dict[str, list[str]], section_names: list[str]) -> None:
        self.data_dict:     dict[str, list[str]] = data_dict
        self.section_names: list[str]            = section_names
        self.formatEpub()

    def _saveFile(self, file_name: str, content: str) -> None:
        EPUBExport.save_counter += 1
        save_counter_str: str = str(EPUBExport.save_counter)
        while len(save_counter_str) < 3:
            save_counter_str = f'0{save_counter_str}'

        file_name = file_name.replace(' ', '')

        folder_dir: str = r"resources\epub_output\ ".strip()    # .strip() is only used because \" is an escape character
        file_dir: str = f"{folder_dir}{save_counter_str}{file_name}.xhtml"

        with open(file_dir, "w", encoding='utf-16') as text_file:
            text_file.write(content)

    def _generateSectionPage(self, header: str) -> str:
        section_html: str = f'''
            <?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html>

            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">
            <head>
                <title>{header}</title>
            <link href="style/style.css" rel="stylesheet" type="text/css"/>
            </head>
            <body dir="auto">
                <h1 dir="ltr" class="center">{header}</h1>
            {EPUBExport.html_tail}
        '''
        
        return section_html
    
    def _genHTMLChapterHeader(self, header: str) -> str:
        html_header: str = f'''
            <?xml version="1.0" encoding="utf-16"?>
            <!DOCTYPE html>
            <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" lang="en" xml:lang="en">
            <head>
                <title>{header}</title>
            </head>
            <body dir="auto">
                <h1>{header}</h1>
        '''

        return html_header

    def _genHTMLChapterBody(self, body: list[str]) -> str:
        html_body: str = ''

        for text in body:
            html_body = f'{html_body}<p>{text}</p>\n'

        return html_body

    def _generateChapterHTML(self, header: str, body: list[str]) -> str:
        html_header: str = self._genHTMLChapterHeader(header)

        html_body: str = self._genHTMLChapterBody(body)

        full_html: str = html_header + html_body + EPUBExport.html_tail

        return full_html

    def formatEpub(self) -> None:
        section_keys: list[str] = list(self.data_dict.keys())

        seperator:       str = '-:-'
        parent_section:  str = ''       # Saves past section's parent
        current_parent_section: str = ''       # Stores current section's parent
        
        for key in section_keys:
            si: int = key.index(seperator)  # Seperator Index
            chapter_name: str = key[si + len(seperator) + 1:]
            print(chapter_name)
            body_content: list[str] = self.data_dict[key]

            if seperator in key:
                current_parent_section = key[:si]
            
            if current_parent_section != parent_section:
                parent_section = current_parent_section

                section_html: str = self._generateSectionPage(current_parent_section)
                self._saveFile(file_name= current_parent_section, content= section_html)

            chapter_html: str = self._generateChapterHTML(header= chapter_name, body= body_content)
            self._saveFile(file_name= chapter_name, content= chapter_html)



