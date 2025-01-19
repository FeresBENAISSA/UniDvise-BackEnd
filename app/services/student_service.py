from datetime import datetime
from typing import List, Optional, Dict

from sqlalchemy.connectors import asyncio

from app.config import Config
from app.models.database import Student, Grade, Activity,Universities,Major
from app.decision_making. university_scoring_system import (
    business_admin_scoring, accounting_scoring, finance_scoring,
    computer_science_scoring, computer_engineering_scoring, mechanics_scoring
)

class StudentService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    async def create_student(self, first_name: str, last_name: str, location: str,password_hash: str ,leadership_position: str,email: str,date_of_birth: Optional[datetime] = None, university_id: Optional[int] = None) -> Student:
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'date_of_birth': date_of_birth,
            'location': location,
            'password_hash': password_hash,
            'leadership_position': leadership_position,
            'university_id': university_id
        }
        result = self.supabase.table('student').insert(data).execute()
        return result.data[0]

    async def get_student_by_id(self, student_id: int) -> Optional[Student]:
        result = self.supabase.table('student').select('*').eq('id', student_id).execute()
        return result.data[0] if result.data else None

    async def get_all_students(self) -> List[Student]:
        result = self.supabase.table('student').select('*').execute()
        return result.data

    async def update_student(self, student_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, email: Optional[str] = None, date_of_birth: Optional[datetime] = None, university_id: Optional[int] = None) -> Optional[Student]:
        data = {}
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if email:
            data['email'] = email
        if date_of_birth:
            data['date_of_birth'] = date_of_birth
        if university_id:
            data['university_id'] = university_id

        if not data:
            return None

        result = self.supabase.table('student').update(data).eq('id', student_id).execute()
        return result.data[0] if result.data else None

    async def delete_student(self, student_id: int) -> bool:
        result = self.supabase.table('student').delete().eq('id', student_id).execute()
        return len(result.data) > 0

    async def get_student_with_grades(self, student_id: int) -> Optional[Dict]:
        """
        Fetch a student by their ID along with their list of grades.

        Returns:
            A dictionary containing the student's details and their grades.
            Example:
            {
                "student": { ...student details... },
                "grades": [ ...list of grades... ]
            }
        """
        try:
            # Fetch the student by ID
            student_result = self.supabase.table('student').select('*').eq('id', student_id).execute()
            if not student_result.data:
                return None  # Student not found

            student = Student(**student_result.data[0])

            # Fetch all grades for the student
            grades_result = self.supabase.table('grade').select('*').eq('student_id', student_id).execute()
            grades = [Grade(**grade) for grade in grades_result.data]

            # Combine student and grades into a single response
            return {
                "student": student.__dict__,
                "grades": [grade.__dict__ for grade in grades]
            }
        except Exception as e:
            print(f"Error fetching student with grades: {e}")
            return None

    async def evaluate_student(self, student_id: int, major_name: str, student_activities: List[Dict]) -> Dict:
        try:
            # Fetch student details
            student_result = self.supabase.table('student').select('*').eq('id', student_id).execute()
            if not student_result.data:
                return {"error": "Student not found"}

            student = Student(**student_result.data[0])

            # Fetch student grades
            grades_result = self.supabase.table('grade').select('*').eq('student_id', student_id).execute()
            grades = {grade['course_name']: grade['grade_value'] for grade in grades_result.data}

            # Use the provided student_activities instead of fetching from the database
            activities = student_activities

            # Fetch all universities
            university_result = self.supabase.table('universities').select('*').execute()
            if not university_result.data:
                return {"error": "No universities found"}

            # Fetch major details
            major_result = self.supabase.table('majors').select('*').eq('name', major_name).execute()
            if not major_result.data:
                return {"error": "Major not found"}

            major = Major(**major_result.data[0])

            # Determine the scoring function based on the major
            scoring_functions = {
                "Business Administration": business_admin_scoring,
                "Accounting": accounting_scoring,
                "Finance": finance_scoring,
                "Computer Science": computer_science_scoring,
                "Computer Engineering": computer_engineering_scoring,
                "Mechanics": mechanics_scoring
            }

            scoring_function = scoring_functions.get(major_name)
            if not scoring_function:
                return {"error": "Scoring function not found for the major"}

            # Fetch all university-major relationships for the given major
            university_major_result = self.supabase.table('university_major') \
                .select('university_id, major_id, minimumscore') \
                .eq('major_id', major.major_id) \
                .execute()

            # Create a dictionary to map university_id to minimum score
            university_min_scores = {
                um['university_id']: um['minimumscore']
                for um in university_major_result.data
            }

            # List to store matching universities
            matching_universities = []

            # Iterate over all universities
            for university_data in university_result.data:
                university = Universities(**university_data)

                # Check if the major is offered at the university
                if university.university_id not in university_min_scores:
                    continue  # Major not offered at this university

                # Get the minimum score for the major at this university
                min_score = university_min_scores[university.university_id]

                # Calculate the student's score for this university
                student_score = scoring_function(grades, activities, student.location, university.location)

                # Check if the student meets the minimum score
                meets_criteria = student_score >= min_score

                # Add the university to the matching list
                matching_universities.append({
                    "university_id": university.university_id,
                    "university_name": university.name,
                    "location": university.location,
                    "student_score": student_score,  # Adjusted score
                    "min_score_required": min_score,
                    "meets_criteria": meets_criteria
                })

            # Sort matching universities by student score (descending order)
            matching_universities.sort(key=lambda x: x['student_score'], reverse=True)

            return {
                "student_id": student_id,
                "major_name": major_name,
                "matching_universities": matching_universities
            }
        except Exception as e:
            print(f"Error evaluating student: {e}")
            return {"error": str(e)}