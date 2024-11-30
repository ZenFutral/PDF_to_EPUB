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
