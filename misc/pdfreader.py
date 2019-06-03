# from PyPDF2 import PdfFileReader
#
# pdf_document = ""
# with open(pdf_document, "rb") as filehandle:
#     pdf = PdfFileReader(filehandle)
#     info = pdf.getDocumentInfo()
#     pages = pdf.getNumPages()
#
#     print (info)
#     print ("number of pages: %i" % pages)
#
#     page1 = pdf.getPage(1)
#     print(page1)
#     print(page1.extractText())

import fitz

pdf_document = "D:/PROJECTS/src/material/Thinking-Clearly.pdf"
doc = fitz.open(pdf_document)
print ("number of pages: %i" % doc.pageCount)
print(doc.metadata)

page1 = doc.loadPage(0)
page1text = page1.getText("text")
print(page1text)