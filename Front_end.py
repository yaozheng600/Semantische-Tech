import streamlit as st
from PIL import Image
import pytesseract
import os
import fitz
import pandas as pd
from time import sleep
import streamlit.components.v1 as components


def img_to_str_tesseract(image_path):
    return pytesseract.image_to_string(Image.open(image_path), lang='deu')


def mkdir(path):
    # remove the space at the begining
    path = path.strip()
    # remove \ at the end
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def tweak(file, old_str, new_str):
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)


def pdf_to_text(uploaded_pdf, imgPath, zoom_x, zoom_y, rotation_angle):
    # open pdf
    pdf = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    # make img path
    mkdir(imgPath)
    # read the pdf by page
    with open(imgPath + '/' + "text.txt", 'w') as f:
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            # set pdf zoom factors
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
            pm = page.getPixmap(matrix=trans, alpha=False)
            # write images
            pm.writePNG(imgPath + '/' + str(pg) + ".png")
            # write text
            f.write(img_to_str_tesseract(imgPath + '/' + str(pg) + '.png'))
    pdf.close()
    tweak(imgPath + '/' + "text.txt", '$', '§')


# def st_display_pdf(pdf_file):
#     with open(pdf_file, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf">'
#     st.markdown(pdf_display, unsafe_allow_html=True)
#
st.title("Text Classification SP SS2021")
"""
## Upload a file 
"""

uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_pdf is not None:
    text = pdf_to_text(uploaded_pdf, r"Test_Court_File_", 5, 5, 0)
    # st_display_pdf(uploaded_pdf)
    agree = st.checkbox('Show the OCR result')
    if agree:
        file_object = open("Test_Court_File_/text.txt")
        try:
            file_context = file_object.read()
        finally:
            file_object.close()
        st.text(file_context)


