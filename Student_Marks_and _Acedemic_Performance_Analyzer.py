import math


def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")
            continue

        if value > 0:
            return value
        print("Please enter a number greater than zero.")


def read_number(prompt, minimum, maximum=None, minimum_inclusive=True):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if not math.isfinite(value):
            print("Please enter a finite number.")
        elif (
            value < minimum
            if minimum_inclusive
            else value <= minimum
        ) or (maximum is not None and value > maximum):
            if not minimum_inclusive:
                print(f"Value must be greater than {minimum}.")
            elif maximum is None:
                print(f"Value must be at least {minimum}.")
            else:
                print(f"Value must be between {minimum} and {maximum}.")
        else:
            return value


def grade_for_mark(mark):
    if mark >= 90:
        return "A+", 4.0
    if mark >= 85:
        return "A", 4.0
    if mark >= 80:
        return "A-", 3.7
    if mark >= 75:
        return "B+", 3.3
    if mark >= 70:
        return "B", 3.0
    if mark >= 65:
        return "B-", 2.7
    if mark >= 60:
        return "C+", 2.3
    if mark >= 55:
        return "C", 2.0
    if mark >= 51:
        return "D", 1.5
    return "F", 0.0


print("===== STUDENT PERFORMANCE ANALYZER =====")

student_name = input("Enter your name: ").strip().title()
subject_count = read_positive_integer("How many subjects do you want to enter? ")

subjects = []
total_marks = 0.0
total_credits = 0.0
weighted_grade_points = 0.0
passed = 0
failed = 0

for subject_number in range(1, subject_count + 1):
    print(f"\nSubject {subject_number}")
    subject_name = input("Enter subject name: ").strip()
    while not subject_name:
        print("Subject name cannot be empty.")
        subject_name = input("Enter subject name: ").strip()

    mark = read_number("Enter marks (0-100): ", 0, 100)
    credit_hours = read_number(
        "Enter credit hours: ", 0, minimum_inclusive=False
    )
    grade, grade_point = grade_for_mark(mark)
    result = "Pass" if grade != "F" else "Fail"

    if result == "Pass":
        passed += 1
    else:
        failed += 1

    subjects.append({
        "name": subject_name,
        "mark": mark,
        "credit_hours": credit_hours,
        "grade": grade,
        "grade_point": grade_point,
        "result": result,
    })
    total_marks += mark
    total_credits += credit_hours
    weighted_grade_points += grade_point * credit_hours

average = total_marks / subject_count
overall_grade, _ = grade_for_mark(average)
sgpa = weighted_grade_points / total_credits

print("\n===== SUBJECT-WISE RESULTS =====")
for subject in subjects:
    print(
        f"{subject['name']}: {subject['mark']:g}/100 | "
        f"Credits: {subject['credit_hours']:g} | "
        f"Grade: {subject['grade']} ({subject['grade_point']} points) | "
        f"{subject['result']}"
    )

report = {
    "Student": student_name,
    "Total Subjects": subject_count,
    "Total Marks": f"{total_marks:g} / {subject_count * 100}",
    "Average": f"{average:.2f} / 100",
    "Overall Grade": overall_grade,
    "Subjects Passed": passed,
    "Subjects Failed": failed,
    "Total Credit Hours": f"{total_credits:g}",
    "SGPA (4.0 scale)": f"{sgpa:.2f}",
}

print("\n===== FINAL ACADEMIC REPORT =====")
for key, value in report.items():
    print(f"{key}: {value}")

if failed == 0:
    print("Excellent! You passed every subject.")
else:
    print("Keep practicing and focus on your weaker subjects.")
