from automagica import *


class Read():
    def __init__(self):
        f_out = open('read_docx/magical.txt', 'w')
        document = OpenWordDocument('read_docx/magical.docx')
        for p in document.paragraphs:
            f_out.write(p.text)
            f_out.close()
