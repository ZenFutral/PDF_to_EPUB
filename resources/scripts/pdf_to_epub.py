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
from epub_exporter import EPUBExport

section_names: list[str] = ["Part", "Chapter"]  # Ordered from top organizational layer downwards (ie Parts > Chapters > Scenes)

def saveToFile(file_name: str, paragraphs: list, include_unicode: bool = False) -> None:
    folder_dir: str = r"resources\scripts\outputs\ ".strip()    # .strip() is only used because \" is an escape character
    file_dir: str = f"{folder_dir}{file_name}"
    with open(file_dir, "w", encoding='utf-16') as text_file:
        for par in paragraphs:
                if isinstance(par, list):
                    par = ' '.join(par)
                
                elif isinstance(par, tuple):
                    par_list = par[1]
                    par_list_as_str = "".join(par_list)
                    par = ' '.join([par[0], par_list_as_str])

                text_file.write(par + '\n')

    if include_unicode:
        with open((file_dir + '_unicode'), "w", encoding='utf-16') as text_file:
            for par in paragraphs:
                if isinstance(par, list):
                    par = ' '.join(par)

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
    
    sections_found: list[str] = pdf_extractor.sections_found
    data:           list[str] = pdf_extractor.new_data

    data_org: DataOrganizer = DataOrganizer(sections_found, data, section_names)
    data_dict: dict = data_org.data_dict

    ebup_formatter: EPUBExport = EPUBExport(data_dict, section_names)

    saveToFile(file_name= r"1_pdf_extractor.txt", paragraphs= data)
    saveToFile(file_name= r"2_data_org.txt", paragraphs= list(data_dict.keys()))

if __name__ == "__main__":
    main()