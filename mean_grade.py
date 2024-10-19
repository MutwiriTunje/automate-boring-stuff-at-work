# Initialize an empty list to store grades
grades = []

# Loop to collect 5 grades as input from the user
for i in range(5):
    grade = input(f"Enter grade {i+1}: ").upper()  # Ensure the input is uppercase
    grades.append(grade)

# Mapping letter grades to numerical values
grade_mapping = {
    'A': 12,
    'A-': 11,
    'B+': 10,
    'B': 9,
    'B-': 8,
    'C+': 7,
    'C': 6,
    'C-': 5,
    'D+': 4,
    'D': 3,
    'D-': 2,
    'E': 1
}

# Reverse mapping to convert numerical mean back to a letter grade
reverse_grade_mapping = {
    (12, 12): 'A',
    (11.0, 11.9): 'A-',
    (10.0, 10.9): 'B+',
    (9.0, 9.9): 'B',
    (8.0, 8.9): 'B-',
    (7.0, 7.9): 'C+',
    (6.0, 6.9): 'C',
    (5.0, 5.9): 'C-',
    (4.0, 4.9): 'D+',
    (3.0, 3.9): 'D',
    (2.0, 2.9): 'D-',
    (1.0, 1.9): 'E'
}

# Convert letter grades to numerical values
numeric_scores = [grade_mapping[grade] for grade in grades]

# Calculate the mean score
mean_score = sum(numeric_scores) / len(numeric_scores)

# Convert the mean score back to a letter grade
for grade_range, letter_grade in reverse_grade_mapping.items():
    if grade_range[0] <= mean_score <= grade_range[1]:
        mean_letter_grade = letter_grade
        break

# Output the result
print(f"The mean letter grade is: {mean_letter_grade}")
print(f"The mean grade is: {mean_score}")
