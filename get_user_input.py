from multiprocessing.connection import answer_challenge

def get_user_input_start_number():
    global document_number
    document_number = input(
                "Please enter the starting exhibit number " 
                + "(Press 'Enter' with no response for 1): ")
    if document_number == "":
        document_number = 1
    else:
        document_number = int(document_number)

def get_user_input_for_party():
    while True:
        global party_type
        party_type = input("Enter 'p' for Petitioner, or 'r' for Respondent (Hit 'Enter' with no response for Petitioner): ")

        if party_type.lower() == 'p':
            party_type = 'p'
            break
        if party_type.lower() == 'r':
            party_type = 'r'
            break
        if party_type == '':
            party_type = 'p'
            break
        else:
            print("The response '" + str(party_type) + "' is not an option.")