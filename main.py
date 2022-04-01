#Local Modules
import get_user_input
#Online Modules
from cgitb import text
from PyPDF2 import PdfFileWriter, PdfFileMerger, PdfFileReader
import glob
import io
import fpdf
import os
import sys

sticker_file = r'resources/exhibit-label.jpg' #sets label picture location
# defines where this blank pdf is located to be modified later
temporary_text_file = r'resources/temporary-text.pdf'
# this references where to find the documents that the user needs labeled
document_folder_path = r'DOCUMENTS-GO-HERE/'
document_number = 1 # sets the starting number for the first document R-"1"
get_user_input.get_user_input_start_number() #get input for starting number

party_type = 'p' #create variable for Party at default of 'p' Petitioner
get_user_input.get_user_input_for_party() # get input for party type

# creates a list with all .pdf files in the directory stored to it
folder_doc_list = list(glob.glob(document_folder_path + '*.pdf'))
print(str(folder_doc_list)) # for debugging purposes

#open notepad files
with open(r'resources/exhibit-list.txt', 'w') as list_text_file:
    list_text_file.write('')
with open(r'resources/success-and-fail-log.txt', 'w') as success_log_text_file:
    success_log_text_file.write('')

#This for loop handles the labeling of each pdf document
for file in folder_doc_list:
    #this variable will decide if the text log shows a SUCCESS or FAIL next
    #to the file name. Placed here to reset value to default of True
    file_successfully_labeled = True

    #get values
    targeted_pdf = PdfFileReader(str(file))
    targeted_pdf_page = targeted_pdf.getPage(0)
    target_pdf_width = float(targeted_pdf_page.mediaBox.getWidth()) * 0.352
    target_pdf_height = float(targeted_pdf_page.mediaBox.getHeight()) * 0.352

    #set label width and height depending on the size of the document that is
    #being labeled
    sticker_width = target_pdf_width / 8
    sticker_height = sticker_width * 0.67924528

    font_size = ((sticker_width + sticker_height) * 14 / 480) * 10

    #sets the text properties that will display on the label
    text_pdf_page = fpdf.FPDF('p', 'mm',
            [target_pdf_width, target_pdf_height])
    text_pdf_page.add_page()
    text_pdf_page.set_font('Times', style='B', size=font_size)
    text_pdf_page.set_xy(5, 5)
    text_pdf_page.image(sticker_file, 0, 0, sticker_width, sticker_height)

    if get_user_input.party_type == 'r':
        text_pdf_page.cell(target_pdf_width / 9, sticker_width * .4,
                txt='R-' + str(get_user_input.document_number).zfill(2), ln=0)

        text_pdf_page.output(temporary_text_file)
    else:
        text_pdf_page.cell(target_pdf_width / 9, sticker_width * .4,
                txt='P-' + str(get_user_input.document_number).zfill(2), ln=0)

        text_pdf_page.output(temporary_text_file)

    text_pdf_page.close()

    overlay_file = PdfFileReader(temporary_text_file)

    target_first_page = targeted_pdf.getPage(0)

    target_first_page.mergePage(overlay_file.getPage(0))

    pdf_writer = PdfFileWriter()
    try:
        for page in targeted_pdf.pages:
            pdf_writer.addPage(page)

        labeled_pdf_file = open(file, 'wb')
        pdf_writer.write(labeled_pdf_file)

        labeled_pdf_file.close()
    except:
        file_successfully_labeled = False

    #gets just the name of the pdf file(and not the directory location)
    # to be used when renaming the file
    name_of_pdf_no_directory = str(file.split("/", 1)[1])
    # The code below goes through each file in DOCUMENTS-GO-HERE and adds
    # P-1 or R-1 (depending on party_type set above) to the start of the file
    if get_user_input.party_type.lower() == 'r':
        #add to exhibit list text file
        with open(r'resources/exhibit-list.txt', 'a') as list_text_file_output:
            list_text_file_output.write("\nRespondents "
                    + str(get_user_input.document_number).zfill(2)
                    + ' - ' + name_of_pdf_no_directory[:-4])
        #rename file
        os.rename(file,
                document_folder_path + "R-"
                        + str(get_user_input.document_number).zfill(2)
                        + '. ' + name_of_pdf_no_directory)   
    else:
        #add to exhibit list text file
        with open(r'resources/exhibit-list.txt', 'a') as list_text_file_output:
            list_text_file_output.write("\nPetitioners "
                    + str(get_user_input.document_number).zfill(2)
                    + ' - ' + name_of_pdf_no_directory[:-4])
        #rename file
        os.rename(file,
                document_folder_path + "P-"
                        + str(get_user_input.document_number).zfill(2)
                        + '. ' + name_of_pdf_no_directory)
    #print SUCCESS or FAIL in the log text file for each document
    if file_successfully_labeled == True:
        with open(r'resources/success-and-fail-log.txt',
                 'a') as log_text_file_output:
            log_text_file_output.write("\nSUCCESS " + str(file))
    else:
        with open(r'resources/success-and-fail-log.txt',
                 'a') as log_text_file_output:
            log_text_file_output.write("\nFAIL " + str(file))

    if get_user_input.document_number >= (
                get_user_input.document_number + len(folder_doc_list)):
        break
    else: 
        get_user_input.document_number += 1