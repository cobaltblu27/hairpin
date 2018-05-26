#!/usr/bin/env python
from docx import Document

SOURCE_PATH = "./src/"

document = Document(SOURCE_PATH + 'seq_short.docx')

for par in document.paragraphs:
    print(par.text)


