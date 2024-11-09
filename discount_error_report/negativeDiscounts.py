import re
import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog

def extract_text_from_pdf(pdf_filename):
    try:
        pdf_file_obj = open(pdf_filename, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            text += page_obj.extract_text()
        pdf_file_obj.close()
        return text
    except FileNotFoundError:
        print(f"Error: File '{pdf_filename}' not found.")
        return None

def extract_values_from_text(text):
    # Define regex patterns
    bill_number_pattern = r'Bill No\. : (\d+)'
    total_paid_pattern = r'Total Paid (\d+\.\d{2})'
    total_incl_pattern = r'Total Incl-(\d+\.\d{2})'

    # Extract relevant values
    bill_number_match = re.search(bill_number_pattern, text)
    total_paid_match = re.search(total_paid_pattern, text)
    total_incl_match = re.search(total_incl_pattern, text)

    if bill_number_match and total_paid_match and total_incl_match:
        bill_number = bill_number_match.group(1)
        total_paid = float(total_paid_match.group(1))
        total_incl = float(total_incl_match.group(1))
        return bill_number, total_paid, total_incl
    else:
        return None

def calculate_difference(total_paid, total_incl):
    return total_incl - total_paid

def choose_output_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    folder_path = filedialog.askdirectory(title="Select Output Folder")
    return folder_path

def choose_pdf_files():
    root =tk.Tk()
    root.withdraw() # Hide the main window

    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    return file_paths


# Usage
pdf_files = choose_pdf_files()
if pdf_files:
    output_folder = choose_output_folder() # choose th output folder once
    if output_folder:
        for pdf_filename in pdf_files:
            extracted_text = extract_text_from_pdf(pdf_filename)
            if extracted_text:
                bill_number, total_paid, total_incl = extract_values_from_text(extracted_text)
                if total_incl == total_paid:
                    print('No discount found')
                    
                else:
                    if total_incl < total_paid:
                        if bill_number and total_paid and total_incl:
                            difference = calculate_difference(total_paid, total_incl)
                            print(f"Bill Number: {bill_number}")
                            print(f"Total Paid: {total_paid:.2f}")
                            print(f"Total Inclusive: {total_incl:.2f}")
                            print(f"Difference: {difference:.2f}")
                            
                            # Save output to a text file
                            output_filename = os.path.join(output_folder, f"{bill_number}.txt")
                            with open(output_filename, 'w') as output_file:
                                output_file.write(f"Bill Number: {bill_number}\n")
                                output_file.write(f"Total Paid: {total_paid:.2f}\n")
                                output_file.write(f"Total Inclusive: {total_incl:.2f}\n")
                                output_file.write(f"Difference: {difference:.2f}\n")
                            print(f"Output saved to {output_filename}")
                        else:
                            print("No relevant information extracted from the PDF.")
            else:
                print(f"Unable to extract relevant information from {pdf_filename}.")
        else:
            print("The end!.")
else:
    print("No PDF files selected.")