from cgitb import text
from PyPDF2 import PdfFileWriter, PdfFileMerger, PdfFileReader
import glob
import io
import fpdf
import os
import sys

sticker_file = r'resources/exhibit-label.jpg'
temporary_text_file = r'resources/temporary-text.pdf'
document_folder_path = r'DOCUMENTS-GO-HERE/'
document_number = 1

party_type = 'r'
'''
for file in os.listdir(document_folder_path):
    if file.endswith('.pdf'):
        if party_type.lower() == 'r':
            os.rename(document_folder_path + '/' + file, 
            document_folder_path + '/' + "R-" + str(document_number).zfill(2) + '. ' + file)
            document_number += 1
        else:
            os.rename(document_folder_path + '/' + file, 
            document_folder_path + '/' + "P-" + str(document_number).zfill(2) + '. ' + file)
            document_number += 1
'''
#print("Jobs done.")

folder_doc_list = list(glob.glob(document_folder_path + '*.pdf'))
print(str(folder_doc_list))

for file in folder_doc_list:
    targeted_pdf = PdfFileReader(str(file))
    targeted_pdf_page = targeted_pdf.getPage(0)
    target_pdf_width = float(targeted_pdf_page.mediaBox.getWidth()) * 0.352
    target_pdf_height = float(targeted_pdf_page.mediaBox.getHeight()) * 0.352

    sticker_width = target_pdf_width / 8
    sticker_height = sticker_width * 0.67924528

    font_size = ((sticker_width + sticker_height) * 14 / 480) * 10

    text_pdf_page = fpdf.FPDF('p', 'mm', [target_pdf_width, target_pdf_height])
    text_pdf_page.add_page()
    text_pdf_page.set_font('Times', style='B', size=font_size)
    text_pdf_page.set_xy(5, 5)
    text_pdf_page.image(sticker_file, 0, 0, sticker_width, sticker_height)

    if party_type == 'r':
        text_pdf_page.cell(target_pdf_width / 9, sticker_width * .4,
        txt='R-' + str(document_number).zfill(2), ln=0)

        text_pdf_page.output(temporary_text_file)
    else:
        text_pdf_page.cell(target_pdf_width / 9, sticker_width * .4,
        txt='P-' + str(document_number).zfill(2), ln=0)

        text_pdf_page.output(temporary_text_file)

    text_pdf_page.close()

    overlay_file = PdfFileReader(temporary_text_file)

    target_first_page = targeted_pdf.getPage(0)

    target_first_page.mergePage(overlay_file.getPage(0))

    pdf_writer = PdfFileWriter()

    for page in targeted_pdf.pages:
        pdf_writer.addPage(page)

    labeled_pdf_file = open(file, 'wb')
    pdf_writer.write(labeled_pdf_file)

    labeled_pdf_file.close()

    

    if document_number >= len(folder_doc_list):
        break
    else: 
        document_number += 1

print("Jobs Done for labeling")