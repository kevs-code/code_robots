from automagica import *


class OcrRead():
    def __init__(self):
        text = ExtractTextFromImage(filename='ocr_text_read/img_text.png')
        f_out = open('ocr_text_read/img_text.txt', 'w')
        f_out.write(text)
        f_out.close()
