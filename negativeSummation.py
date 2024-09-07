import re
import os
import tkinter as tk
from tkinter import filedialog

def extract_values_from_text(text):
    # Define regex patterns
    difference_pattern = r'Difference: -(\d+\.\d{2})'

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
                    Total_discounts += float(difference)
                    
                else:
                    print(f'No relevant information found in {file_path}')
        except FileNotFoundError:
            print(f'Error reading {file_path}')
    print(f"Total unaccounted discounts across all files: {Total_discounts:.2f}")
else:
    print("No files selected")