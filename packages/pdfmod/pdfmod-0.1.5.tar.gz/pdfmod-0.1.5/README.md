# 🚀 PdfMod

## 🌟 Overview

PdfMod is a tool for manipulating PDF files, utilizing the [pymupdf](https://github.com/pymupdf/PyMuPDF) library. It enables reading and writing the table of contents, deleting pages, merging PDF files, and extracting pages. PdfMod facilitates the management and modification of PDF files according to your requirements.

## 📦 Dependencies

> [!NOTE]
> PdfMod requires Python 3.7 or higher.

## 💻 Installation

To install PdfMod, run the following command in your terminal:

```
pip install pdfmod
```

## 🚀 Basic Usage

### Reading a PDF's Table of Contents

To read a PDF file's table of contents and open it in a text editor, use the following command:

```
pdfmod toc read "D:\\如何提问.pdf" notepad
```

This command will extract the table of contents from the PDF file and open it in Notepad.

### Writing to a PDF's Table of Contents

To write a table of contents to a PDF file, use the following command:

```
pdfmod toc write "D:\\如何提问.pdf" --bias=8
```

This command will write the table of contents to the PDF file
with a bias of 8.

The `--bias` option is used to adjust the position of the table of contents within the PDF file. A bias of 8 means that the table of contents will be shifted 8 units to the right from its default position. This can be useful for aligning the table of contents with the content of the PDF file.

### Deleting Pages from a PDF

To delete pages from a PDF file, use the following command:

```
pdfmod delete "D:\\如何提问.pdf" 0 25
```

This command will delete pages 0 through 25 from the PDF file.

### Joining PDF Files

To merge two PDF files, use the following command:

```
pdfmod join "D:\\如何提问_上半.pdf" "D:\\如何提问_下半.pdf"
```

This command will merge the two PDF files into a single PDF file.

###  Extracting Pages from a PDF

To extract pages from a PDF file and save them as a new PDF, use the following command:

```
pdfmod extract "D:\\如何提问.pdf" 0 25
```

This command will extract pages 0 through 25 from the PDF file and save them as a new PDF file.
