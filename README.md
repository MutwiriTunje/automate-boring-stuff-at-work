This scripts takes a cash receipt in pdf format
asks for the file path
runs the code and asks for the destination folder

what does it do?
i made this script to go through the cash receipt and return the following: bill number, total amount paid, total inclusive and the difference between the two totals.
the information is stored in a txt file in the designated folder and the file name is the bill number 

problem statement:
we discovered a number of cash sales were done where the sales discount-on the total paid- did not reflect on the total inclusive which is the report that goes to KRA.
so i made this script to automate the work and find the discrepancies in the amounts.

usage:
first install the requirements like so
pip install -r requirements.txt
and you are good to go
i've included two samples: test.pdf and test1.pdf
