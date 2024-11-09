
# Cash Receipt Analysis Script

This script automates the analysis of cash receipts in PDF format, extracting specific details and identifying discrepancies. It prompts the user for the file path of the PDF receipt and the destination folder to store the results.

## Overview

This tool was developed to:
1. Extract details from cash receipts, including:
   - Bill Number
   - Total Amount Paid
   - Total Inclusive Amount
   - The difference between the Total Paid and Total Inclusive amounts
2. Store this information in a `.txt` file, saved in the specified destination folder with the bill number as the filename.

### Problem Statement

During routine checks, discrepancies were identified in cash sales reports. Specifically, sales discounts applied to the *Total Paid* were not consistently reflected in the *Total Inclusive* amount, which is reported to the Kenya Revenue Authority (KRA). This script was created to automate the detection of these inconsistencies by analyzing and calculating any differences.

## Usage

1. **Install Requirements**  
   Before running the script, install the necessary packages by executing:
   ```bash
   pip install -r requirements.txt
   ```

2. **Running the Script**  
   When prompted:
   - Provide the file path for the PDF receipt.
   - Specify the destination folder where you’d like the `.txt` output to be saved.

3. **Output**  
   - The script generates a `.txt` file in the chosen folder, named after the bill number. This file contains:
     - Bill Number
     - Total Amount Paid
     - Total Inclusive Amount
     - Difference between Total Paid and Total Inclusive

### Example

A sample PDF (`test.pdf`) is included for testing purposes.

## Requirements

- Python 3.x
- The libraries listed in `requirements.txt`
