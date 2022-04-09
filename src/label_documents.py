def log_output_success(file_successfully_labeled, file):
        #print SUCCESS or FAIL in the log text file for each document
        if file_successfully_labeled == True:
            output_text_for_log = "SUCCESS " + str(file) #helpful for testing
            with open(r'resources/success-and-fail-log.txt',
                    'a') as log_text_file_output:
                log_text_file_output.write("\n" + output_text_for_log)
            return output_text_for_log
                
        else:
            output_text_for_log = "FAIL " + str(file) #helpful for testing
            with open(r'resources/success-and-fail-log.txt',
                    'a') as log_text_file_output:
                log_text_file_output.write("\n" + output_text_for_log)

            return output_text_for_log