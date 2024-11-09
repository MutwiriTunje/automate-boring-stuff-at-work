KCPE Mean Grade Calculator
This script calculates the overall mean grade for Kenya Certificate of Primary Education (KCPE) results. It takes subject grades as input (e.g., A, B, C+), converts them into numerical values, and returns the calculated mean grade as a final output (e.g., B+).

Features
Grade Conversion: Converts letter grades (e.g., A, B, C+) to numerical values based on the standard KCPE grading system.
Mean Calculation: Computes the mean of the provided subject grades and returns the overall mean grade as a single letter grade.
Simple Interface: Input grades in a list format, and the script outputs the overall mean grade in a straightforward manner.
Usage
Input: Provide the KCPE grades for each subject (e.g., A, B, C+, etc.) as a list to the script.
Processing: The script converts each grade into a numerical value, computes the average, and translates the result back to a letter grade.
Output: The final result will be the overall mean grade, displayed as a letter grade (e.g., B+).
Example
python
Copy code
# Sample list of KCPE grades
grades = ["A", "B", "C+", "A-", "B+"]

# Calculating the mean grade
mean_grade = calculate_mean_grade(grades)
print("Overall Mean Grade:", mean_grade)  # Output: Overall Mean Grade: B+
Grade Conversion Table
Grade	Numerical Value
A	12
A-	11
B+	10
B	9
B-	8
C+	7
C	6
C-	5
D+	4
D	3
D-	2
E	1
The script uses these values for calculating the mean and then translates the numerical mean back into a letter grade.

Installation
Clone this repository and ensure you have Python installed.

bash
Copy code
git clone https://github.com/mutwiritunje/automate-boring-stuff-at-work.git
cd mean_grade_finder
Requirements
Python 3.x
Contributing
If you'd like to contribute, please fork the repository, make your changes, and submit a pull request.

