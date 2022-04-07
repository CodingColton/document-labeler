#Local Modules
import get_user_input
#Online Modules
from cgitb import text
from PyPDF2 import PdfFileWriter, PdfFileMerger, PdfFileReader
import glob
import fpdf
import os

# get file locations
sticker_file = r'resources/exhibit-label.jpg'
temporary_text_file = r'resources/temporary-text.pdf'
document_folder_path = r'DOCUMENTS-GO-HERE/'

# set exhibit number default and get user input
document_number = 1 
get_user_input.get_user_input_start_number() 

# set party default and get user input
party_type = 'p' 
get_user_input.get_user_input_for_party() 

# create a list with all .pdf files in the directory stored to it
folder_doc_list = list(glob.glob(document_folder_path + '*.pdf'))
print(str(folder_doc_list)) # for debugging purposes

#open notepad files
with open(r'resources/exhibit-list.txt', 'w') as list_text_file:
    list_text_file.write('')
with open(r'resources/success-and-fail-log.txt', 'w') as success_log_text_file:
    success_log_text_file.write('')

#Label each document in list
for file in folder_doc_list:
    #this variable will decide if the text log shows a SUCCESS or FAIL next
    #to the file name. Set here to reset value to default of True for each loop
    file_successfully_labeled = True

    targeted_pdf = PdfFileReader(str(file))
    targeted_pdf_page = targeted_pdf.getPage(0)
    target_pdf_width = float(targeted_pdf_page.mediaBox.getWidth()) * 0.352
    target_pdf_height = float(targeted_pdf_page.mediaBox.getHeight()) * 0.352

    #set label width and height depending on the size of the document that is
    #being labeled
    sticker_width = target_pdf_width / 8
    sticker_height = sticker_width * 0.67924528

    font_size = ((sticker_width + sticker_height) * 14 / 480) * 10

    #set the text properties that will display on the label
    text_pdf_page = fpdf.FPDF('p', 'mm',
            [target_pdf_width, target_pdf_height])
    text_pdf_page.add_page()
    text_pdf_page.set_font('Times', style='B', size=font_size)
    text_pdf_page.set_xy(5, 5)
    text_pdf_page.image(sticker_file, 0, 0, sticker_width, sticker_height)

    #write text on the label
    if get_user_input.party_type == 'r':
        text_pdf_page.cell(target_pdf_width / 9,
                sticker_width * .4,
                txt='R-' + str(get_user_input.document_number).zfill(2), ln=0)

        text_pdf_page.output(temporary_text_file)
    else:
        text_pdf_page.cell(target_pdf_width / 9,
                sticker_width * .4,
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

    #gets only the name of the pdf file(and not the directory location)
    name_of_pdf_no_directory = str(file.split("/", 1)[1])
    # Rename the file
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