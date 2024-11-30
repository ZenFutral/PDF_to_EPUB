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
from data_cleaner import DataCleaner
from data_organizer import DataOrganizer
from epub_formatter import EPUBFormatter

section_names: list[str] = ["Part", "Chapter"]  # Ordered from top organizational layer downwards (ie Parts > Chapters > Scenes)



def saveToFile(file_name: str, paragraphs: list[str]) -> None:
    with open(file_name, "w", encoding='utf-16') as text_file:
        for par in paragraphs:
            text_file.write(par + '\n')
    
    with open((file_name + '_repr'), "w", encoding='utf-16') as text_file:
        for par in paragraphs:
            text_file.write(repr(par + '\n'))

def main() -> None:
    file_name: str = r"resources\test_pdfs\1984.pdf"
    document = pymupdf.open(file_name, filetype = '.pdf',)

    pdf_extractor: PDFExtractor = PDFExtractor(title = "1984", header_len = 2)
    pdf_data: list[str] = pdf_extractor.extractData(pages = document)

    data_cleaner: DataCleaner = DataCleaner()
    clean_data: list[str] = data_cleaner.cleanData(pdf_data)

    data_org: DataOrganizer = DataOrganizer(section_names=section_names)
    output_tuple: tuple = data_org.extractBookData(clean_data)
    data: list[str] = output_tuple[0]
    sections: list[str] = output_tuple[1]

    for sec in sections:
        if sec in data:
            datai = data.index(sec)
            print(data[datai])

    #form_epub: EPUBFormatter = EPUBFormatter()
    #formatted_data = form_epub.formatEpub(clean_data)

    saveToFile(file_name= r"output.txt", paragraphs= data)

if __name__ == "__main__":
    main()