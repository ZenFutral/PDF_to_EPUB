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
from pdf_extractor import PDFExtractor
from data_organizer import DataOrganizer
from epub_formatter import EPUBFormatter

section_names: list[str] = ["Part", "Chapter"]  # Ordered from top organizational layer downwards (ie Parts > Chapters > Scenes)

def saveToFile(file_name: str, paragraphs: list, include_unicode: bool = False) -> None:
    folder_dir: str = r"resources\scripts\outputs\ ".strip()
    file_dir: str = f"{folder_dir}{file_name}"
    with open(file_dir, "w", encoding='utf-16') as text_file:
        for par in paragraphs:
            text_file.write(par + '\n')

    if include_unicode:
        with open((file_dir + '_unicode'), "w", encoding='utf-16') as text_file:
            for par in paragraphs:
                text_file.write(repr(par + '\n'))

def main() -> None:
    file_name: str = r"resources\test_pdfs\1984.pdf"
    document = pymupdf.open(file_name, filetype = '.pdf',)

    pdf_extractor: PDFExtractor = PDFExtractor(
        pages= document, 
        section_types= section_names, 
        title_pages_len= 1, 
        title = "1984", 
        header_len = 2
    )
    
    pdf_data: list[str] = pdf_extractor.extractData()
    sections_found: list[str] = pdf_extractor.sections_found
    clean_data: list[str] = pdf_extractor.cleanData(pdf_data)

    #data_org: DataOrganizer = DataOrganizer(section_names= section_names, data= clean_data)
    #output_tuple: tuple = data_org.extractBookData()
    #data: list[str] = output_tuple[0]
    #sections: list[tuple[str, int]] = output_tuple[1]

    saveToFile(file_name= r"1_pdf_extractor.txt", paragraphs= pdf_data)
    saveToFile(file_name= r"2_data_cleaner.txt", paragraphs= clean_data)
    #saveToFile(file_name= r"3_data_org.txt", paragraphs= data)

if __name__ == "__main__":
    main()