# First import typing and the required classes
from typing import List, Dict
from university_classes import University, Student, Major
from university_classes import (
    business_admin_scoring, accounting_scoring, finance_scoring,
    computer_science_scoring, computer_engineering_scoring, mechanics_scoring
)


def create_sample_data():
    # Create majors
    business = Major("Business Administration", 100, business_admin_scoring)
    accounting = Major("Accounting", 80, accounting_scoring)
    finance = Major("Finance", 70, finance_scoring)
    cs = Major("Computer Science", 120, computer_science_scoring)
    ce = Major("Computer Engineering", 90, computer_engineering_scoring)
    mechanics = Major("Mechanics", 60, mechanics_scoring)

    # Create universities
    universities = [
        University(
            "Stanford University",
            1000,
            "California, USA",
            [business, finance, cs, ce],
            {
                "Business Administration": 85,
                "Finance": 88,
                "Computer Science": 90,
                "Computer Engineering": 88
            }
        ),
        University(
            "MIT",
            800,
            "Massachusetts, USA",
            [cs, ce, mechanics],
            {
                "Computer Science": 92,
                "Computer Engineering": 90,
                "Mechanics": 88
            }
        ),
        University(
            "Harvard University",
            900,
            "Massachusetts, USA",
            [business, finance, accounting],
            {
                "Business Administration": 88,
                "Finance": 90,
                "Accounting": 86
            }
        )
    ]

    # Create a sample student
    student_grades = {
        'Mathematics': 95,
        'Economics': 88,
        'Philosophy': 85,
        'Computer Science': 92,
        'Physics': 90,
        'Chemistry': 87
    }

    student_activities = [
        {'name': 'Robotics Club', 'position': 'Leader'},
        {'name': 'Computer Programming Society', 'position': 'Member'},
        {'name': 'Finance Club', 'position': 'Leader'},
        {'name': 'Chess Club', 'position': 'Member'}
    ]

    student = Student(
        "John Doe",
        student_grades,
        student_activities,
        "California, USA",
        cs  # Applying for Computer Science
    )

    return universities, student


def find_matching_universities(student: Student, universities: List[University]) -> List[tuple]:
    matches = []

    # Calculate student's score for each university
    for university in universities:
        if student.major in university.majors:
            student.calculate_score(student.major, university.location)
            if student.meets_criteria(university):
                min_score = university.get_min_score_for_major(student.major.name)
                matches.append((university, min_score, student.score))

    # Sort by minimum score in descending order
    return sorted(matches, key=lambda x: x[1], reverse=True)


def print_results(student: Student, matches: List[tuple]):
    print(f"\nResults for {student.name}")
    print(f"Major: {student.major}")
    print(f"Location: {student.location}")
    print("\nQualifying Universities (in order of prestige):")

    if not matches:
        print("No matching universities found.")
        return

    for university, min_score, student_score in matches:
        print(f"\n{university.name}")
        print(f"Location: {university.location}")
        print(f"Minimum Required Score: {min_score}")
        print(f"Student's Score: {student_score:.2f}")

    # The first university in the sorted list is the most prestigious one where the student qualifies
    best_match = matches[0]
    print(f"\nBest Match: {best_match[0].name}")
    print(f"This is the most prestigious university where you meet the requirements.")


def main():
    # Create sample data
    universities, student = create_sample_data()

    # Find matching universities
    matches = find_matching_universities(student, universities)

    # Print results
    print_results(student, matches)


if __name__ == "__main__":
    main()