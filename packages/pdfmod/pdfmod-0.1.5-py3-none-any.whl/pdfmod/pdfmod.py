import fire
import fitz
import os


def toc2file(toc: list, file_path: str) -> None:
    """
    Writes the table of contents to a file.
    
    Args:
        toc (list): The table of contents.
        file_path (str): The path to the file where the toc will be written.
    """
    with open(file_path, "w", encoding='utf-8') as f:
        for item in toc:
            item[0] = str(item[0])
            item[-1] = str(item[-1])
            f.write(" ".join(item) + "\n")


def file2toc(file_path: str) -> list:
    """
    Reads the table of contents from a file.
    
    Args:
        file_path (str): The path to the file from which the toc will be read.
    
    Returns:
        list: The table of contents.
    """
    toc = []
    with open(file_path,encoding='utf-8') as f:
        for line in f:
            items = line.split(" ")
            lvl = int(items[0])
            if items[-1][-1] == "\n":
                items[-1] = items[-1][:-1]
            pn = int(items[-1])
            cn = " ".join(items[1:-1])
            toc.append([lvl, cn, pn])
    return toc


class Toc:
    def read(self, pdf_path: str, editor: str = None) -> None:
        """
        Reads the table of contents from a PDF file and writes it to a .toc file.
        Optionally, opens the .toc file in an editor.
        
        Args:
            pdf_path (str): The path to the PDF file.
            editor (str, optional): The editor to use to open the .toc file. Defaults to None.
        """
        doc = fitz.open(pdf_path)
        toc = doc.get_toc()
        toc_path = pdf_path.replace(".pdf", ".toc")
        toc2file(toc, toc_path)
        if editor:
            os.system(f"{editor} {toc_path}")

    def write(self, pdf_path: str, bias: int = 0) -> None:
        """
        Writes the table of contents to a PDF file, optionally adjusting the page numbers.
        
        Args:
            pdf_path (str): The path to the PDF file.
            bias (int, optional): The bias to apply to the page numbers. Defaults to 0.
        """
        toc_path = pdf_path.replace(".pdf", ".toc")
        if os.path.exists(toc_path):
            doc = fitz.open(pdf_path)
            toc = file2toc(toc_path)
            for item in toc:
                item[-1] += bias
            doc.set_toc(toc)
            doc.saveIncr()
        else:
            print("the toc file doesn't exist.")


class PdfMod:
    def __init__(self) -> None:
        """
        Initializes the PdfMod class.
        """
        self.toc = Toc()

    def delete(self, pdf_path: str, start_pn: int, end_pn: int) -> None:
        """
        Deletes pages from a PDF file.
        
        Args:
            pdf_path (str): The path to the PDF file.
            start_pn (int): The starting page number.
            end_pn (int): The ending page number.
        """
        doc = fitz.open(pdf_path)
        doc.delete_pages(list(range(start_pn-1, end_pn)))
        doc.saveIncr()

    def join(self, *pdfs_path: str) -> None:
        """
        Joins multiple PDF files into one.
        
        Args:
            *pdfs_path (str): The paths to the PDF files to be joined.
        """
        doc = fitz.open(pdfs_path[0])
        for i in pdfs_path[1:]:
            item = fitz.open(i)
            doc.insert_pdf(item)
        doc.saveIncr()

    def extract(self, pdf_path: str, start_pn: int, end_pn: int) -> None:
        """
        Extracts pages from a PDF file and saves them as a new PDF.
        
        Args:
            pdf_path (str): The path to the original PDF file.
            start_pn (int): The starting page number.
            end_pn (int): The ending page number.
        """
        doc = fitz.open(pdf_path)
        pages = [doc[i] for i in range(start_pn-1, end_pn)]
        new_doc = fitz.open()
        for page in pages:
            new_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_doc[-1].show_pdf_page(page.rect, doc, page.number)
        output_path = f"{pdf_path.replace('.pdf', '')}-{start_pn}-{end_pn}.pdf"
        new_doc.save(output_path)


def main():

    fire.Fire(PdfMod)
