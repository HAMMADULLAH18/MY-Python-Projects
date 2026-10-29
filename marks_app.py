
import streamlit as st
import csv
import io

# -----------------------------
# 1. PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# 2. ORIGINAL GRADING FUNCTION
# -----------------------------
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


# -----------------------------
# 3. PAGE TITLE
# -----------------------------
st.title("🎓 Student Marks & Academic Performance Analyzer")
st.write(
    "Enter your marks and credit hours to calculate your "
    "grades, academic performance, and SGPA."
)

st.info(
    "Grading rules are based on the original Python project. "
    "Confirm that these rules match your institution's policy."
)

# Keep results after Streamlit reruns
if "academic_report" not in st.session_state:
    st.session_state.academic_report = None

# -----------------------------
# 4. STUDENT INFORMATION
# -----------------------------
st.header("👤 Student Information")

student_name = st.text_input(
    "Enter student name",
    placeholder="e.g., Hassan"
)

subject_count = st.number_input(
    "How many subjects do you want to enter?",
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

# -----------------------------
# 5. SUBJECT INPUT FORM
# -----------------------------
st.header("📝 Enter Subject Details")

with st.form("marks_form"):
    subject_inputs = []

    for i in range(int(subject_count)):
        st.subheader(f"Subject {i + 1}")

        col1, col2, col3 = st.columns(3)

        with col1:
            subject_name = st.text_input(
                "Subject name",
                key=f"subject_name_{i}",
                placeholder="e.g., Python"
            )

        with col2:
            mark = st.number_input(
                "Marks (out of 100)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=1.0,
                key=f"marks_{i}"
            )

        with col3:
            credits = st.number_input(
                "Credit hours",
                min_value=0.0,
                max_value=10.0,
                value=3.0,
                step=0.5,
                key=f"credits_{i}"
            )

        subject_inputs.append({
            "name": subject_name.strip(),
            "mark": mark,
            "credit_hours": credits
        })

    submitted = st.form_submit_button(
        "📊 Calculate Academic Results",
        type="primary",
        use_container_width=True
    )

# -----------------------------
# 6. VALIDATE AND CALCULATE
# -----------------------------
if submitted:
    if not student_name.strip():
        st.error("Please enter the student's name.")

    elif any(not subject["name"] for subject in subject_inputs):
        st.error("Please enter a name for every subject.")

    elif any(subject["credit_hours"] <= 0 for subject in subject_inputs):
        st.error("Credit hours must be greater than zero.")

    else:
        results = []
        total_marks = 0.0
        total_credits = 0.0
        weighted_grade_points = 0.0
        passed = 0
        failed = 0

        for subject in subject_inputs:
            mark = subject["mark"]
            credits = subject["credit_hours"]

            grade, grade_point = grade_for_mark(mark)
            result = "Pass" if grade != "F" else "Fail"

            if result == "Pass":
                passed += 1
            else:
                failed += 1

            results.append({
                "Subject": subject["name"],
                "Marks": mark,
                "Credit Hours": credits,
                "Grade": grade,
                "Grade Point": grade_point,
                "Result": result
            })

            total_marks += mark
            total_credits += credits
            weighted_grade_points += grade_point * credits

        average = total_marks / len(results)
        overall_grade, _ = grade_for_mark(average)
        sgpa = weighted_grade_points / total_credits

        st.session_state.academic_report = {
            "student_name": student_name.strip().title(),
            "results": results,
            "total_marks": total_marks,
            "maximum_marks": len(results) * 100,
            "average": average,
            "overall_grade": overall_grade,
            "passed": passed,
            "failed": failed,
            "total_credits": total_credits,
            "sgpa": sgpa
        }

# -----------------------------
# 7. DISPLAY ACADEMIC REPORT
# -----------------------------
report = st.session_state.academic_report

if report is not None:
    st.divider()
    st.header(
        f"📊 Academic Report: {report['student_name']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Marks",
        f"{report['total_marks']:g} / {report['maximum_marks']:g}"
    )
    col2.metric(
        "Average",
        f"{report['average']:.2f}%"
    )
    col3.metric(
        "Overall Grade",
        report["overall_grade"]
    )
    col4.metric(
        "SGPA (4.0 scale)",
        f"{report['sgpa']:.2f}"
    )

    st.subheader("📚 Subject-wise Results")
    st.dataframe(
        report["results"],
        use_container_width=True,
        hide_index=True
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Subjects", len(report["results"]))
    col2.metric("Subjects Passed", report["passed"])
    col3.metric("Subjects Failed", report["failed"])

    st.subheader("💳 Credit Hour Summary")
    st.write(f"Total credit hours: {report['total_credits']:g}")

    if report["failed"] == 0:
        st.success("Excellent! You passed every subject.")
    else:
        st.warning(
            f"You have {report['failed']} failed subject(s). "
            "Focus on improving those subjects."
        )

    st.subheader("⬇️ Download Your Academic Report")

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)

    writer.writerow(["Student Academic Report"])
    writer.writerow(["Student Name", report["student_name"]])
    writer.writerow(["Total Marks", report["total_marks"]])
    writer.writerow(["Maximum Marks", report["maximum_marks"]])
    writer.writerow(["Average", f"{report['average']:.2f}"])
    writer.writerow(["Overall Grade", report["overall_grade"]])
    writer.writerow(["Subjects Passed", report["passed"]])
    writer.writerow(["Subjects Failed", report["failed"]])
    writer.writerow(["Total Credit Hours", report["total_credits"]])
    writer.writerow(["SGPA", f"{report['sgpa']:.2f}"])
    writer.writerow([])
    writer.writerow([
        "Subject", "Marks", "Credit Hours",
        "Grade", "Grade Point", "Result"
    ])

    for subject in report["results"]:
        writer.writerow([
            subject["Subject"],
            subject["Marks"],
            subject["Credit Hours"],
            subject["Grade"],
            subject["Grade Point"],
            subject["Result"]
        ])

    st.download_button(
        label="📥 Download Academic Report (CSV)",
        data=csv_buffer.getvalue(),
        file_name="student_academic_report.csv",
        mime="text/csv",
        use_container_width=True
    )
