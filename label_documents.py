def log_output_success(file_successfully_labeled, file):
        #print SUCCESS or FAIL in the log text file for each document
        if file_successfully_labeled == True:
            with open(r'resources/success-and-fail-log.txt',
                    'a') as log_text_file_output:
                log_text_file_output.write("\nSUCCESS " + str(file))
        else:
            with open(r'resources/success-and-fail-log.txt',
                    'a') as log_text_file_output:
                log_text_file_output.write("\nFAIL " + str(file))