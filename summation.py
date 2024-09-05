import re
import os
import tkinter as tk
from tkinter import filedialog

def extract_values_from_text(text):
    # Define regex patterns
    difference_pattern = r'Difference: (\d+\.\d{2})'

    # Extract relevant values
    difference_match = re.search(difference_pattern, text)


    if difference_match:
        difference = difference_match.group(1)
        return difference
    else:
        return None
    
def addition(difference):
    return difference

def choose_files():
    root = tk.Tk()
    root.withdraw() 

    file_paths = filedialog.askopenfilenames(filetypes=[('Text files', '*.txt')])
    return file_paths

try:
    extracted_text_files = choose_files()
except FileNotFoundError:
    print("Error: File not found")
    extracted_text_files = []


if extracted_text_files:
    Total_discounts = 0.0
    for file_path in extracted_text_files:
        try:
            with open(file_path,'r') as file:
                extracted_text = file.read()
                difference = extract_values_from_text(extracted_text)
                if difference:
                    Total_discounts += int(difference)
                    
                else:
                    print(f'No relevant information found in {file_path}')
        except FileNotFoundError:
            print(f'Error reading {file_path}')
    print(f"Total unaccounted discounts across all files: {Total_discounts:.2f}")
else:
    print("No files selected")
                

# import re
# import PyPDF2

# def extract_text_from_pdf(pdf_filename):
#     try:
#         pdf_file_obj = open(pdf_filename, 'rb')
#         pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
#         text = ''
#         for page_num in range(len(pdf_reader.pages)):
#             page_obj = pdf_reader.pages[page_num]
#             text += page_obj.extract_text()
#         pdf_file_obj.close()
#         return text
#     except FileNotFoundError:
#         print(f"Error: File '{pdf_filename}' not found.")
#         return None

# def extract_values_from_text(text):
#     # Define regex patterns
#     bill_number_pattern = r'Bill No\. : (\d+)'
#     total_paid_pattern = r'Total Paid (\d+\.\d{2})'
#     total_incl_pattern = r'Total Incl-(\d+\.\d{2})'

#     # Extract relevant values
#     bill_number_match = re.search(bill_number_pattern, text)
#     total_paid_match = re.search(total_paid_pattern, text)
#     total_incl_match = re.search(total_incl_pattern, text)

#     if bill_number_match and total_paid_match and total_incl_match:
#         bill_number = bill_number_match.group(1)
#         total_paid = float(total_paid_match.group(1))
#         total_incl = float(total_incl_match.group(1))
#         return bill_number, total_paid, total_incl
#     else:
#         return None

# def calculate_difference(total_paid, total_incl):
#     return total_incl - total_paid

# # Usage
# pdf_filename = 'test1.pdf'  # Replace with the actual PDF file path
# extracted_text = extract_text_from_pdf(pdf_filename)

# if extracted_text:
#     bill_number, total_paid, total_incl = extract_values_from_text(extracted_text)
#     if bill_number and total_paid and total_incl:
#         difference = calculate_difference(total_paid, total_incl)
#         print(f"Bill Number: {bill_number}")
#         print(f"Total Paid: {total_paid:.2f}")
#         print(f"Total Inclusive: {total_incl:.2f}")
#         print(f"Difference: {difference:.2f}")
#     else:
#         print("Unable to extract relevant information.")
# else:
#     print("Error occurred while extracting text from the PDF.")