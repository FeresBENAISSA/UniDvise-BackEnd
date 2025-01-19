from typing import List, Optional, Dict
from datetime import datetime
from supabase import Client
from app.config import Config
from app.models.database import Universities, Student, Major, Grade, Activity

class UniversityService:
    def __init__(self):
        self.supabase = Config.init_supabase()

    def get_all_universities(self) -> List[Universities]:
        """Fetch all universities from the database."""
        try:
            result = self.supabase.table('universities').select('*').execute()
            return [Universities(**university) for university in result.data]
        except Exception as e:
            print(f"Error fetching universities: {e}")
            return []

    def get_university_by_id(self, university_id: int) -> Optional[Universities]:
        """Fetch a university by its ID."""
        try:
            result = self.supabase.table('universities').select('*').eq('university_id', university_id).execute()
            return Universities(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error fetching Universities with ID {university_id}: {e}")
            return None

    def create_university(self, name: str, location: str) -> Optional[Universities]:
        """Create a new Universities."""
        try:
            data = {
                'name': name,
                'location': location,
            }
            result = self.supabase.table('universities').insert(data).execute()
            return Universities(**result.data[0])
        except Exception as e:
            print(f"Error creating Universities: {e}")
            return None

    def update_university(self, university_id: int, name: Optional[str] = None, location: Optional[str] = None ) -> Optional[Universities]:
        """Update an existing Universities."""
        try:
            data = {}
            if name:
                data['name'] = name
            if location:
                data['location'] = location



            if not data:
                return None

            result = self.supabase.table('universities').update(data).eq('university_id', university_id).execute()
            return Universities(**result.data[0]) if result.data else None
        except Exception as e:
            print(f"Error updating university with ID {university_id}: {e}")
            return None

    def delete_university(self, university_id: int) -> bool:
        """Delete a university by its ID."""
        try:
            result = self.supabase.table('universities').delete().eq('university_id', university_id).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error deleting university with ID {university_id}: {e}")
            return False

    def get_university_students(self, university_id: int) -> List[Student]:
        """Fetch all students belonging to a specific university."""
        try:
            result = self.supabase.table('student').select('*').eq('university_id', university_id).execute()
            return [Student(**student) for student in result.data]
        except Exception as e:
            print(f"Error fetching students for university with ID {university_id}: {e}")
            return []

    def get_university_majors(self, university_id: int) -> List[Major]:
        """Fetch all majors offered by a specific university."""
        try:
            result = self.supabase.table('university_major').select('major_id').eq('university_id', university_id).execute()
            major_ids = [row['major_id'] for row in result.data]
            majors = []
            for major_id in major_ids:
                major_result = self.supabase.table('major').select('*').eq('major_id', major_id).execute()
                if major_result.data:
                    majors.append(Major(**major_result.data[0]))
            return majors
        except Exception as e:
            print(f"Error fetching majors for university with ID {university_id}: {e}")
            return []

    def get_university_activities(self, university_id: int) -> List[Activity]:
        """Fetch all activities associated with a specific university."""
        try:
            result = self.supabase.table('activity').select('*').eq('university_id', university_id).execute()
            return [Activity(**activity) for activity in result.data]
        except Exception as e:
            print(f"Error fetching activities for university with ID {university_id}: {e}")
            return []

    def get_university_grades(self, university_id: int) -> List[Grade]:
        """Fetch all grades for students belonging to a specific university."""
        try:
            students = self.get_university_students(university_id)
            if not students:
                return []

            student_ids = [student.id for student in students]
            result = self.supabase.table('grade').select('*').in_('student_id', student_ids).execute()
            return [Grade(**grade) for grade in result.data]
        except Exception as e:
            print(f"Error fetching grades for university with ID {university_id}: {e}")
            return []

    def get_university_details(self, university_id: int) -> Optional[Dict]:
        """
        Fetch a university by its ID along with:
        - A list of students enrolled in the university.
        - Each student's list of grades.
        - A list of majors offered by the university, including maxCapacity and minimumScore.

        Returns:
            A dictionary containing the university's details, students, their grades, and majors.
            Example:
            {
                "university": { ...university details... },
                "students": [
                    {
                        "student": { ...student details... },
                        "grades": [ ...list of grades... ]
                    },
                    ...
                ],
                "majors": [
                    {
                        "major_id": 1,
                        "name": "Computer Science",
                        "maxCapacity": 100,
                        "minimumScore": 80,
                        "created_at": "2023-10-01T12:00:00"
                    },
                    ...
                ]
            }
        """
        try:
            # Fetch the university by ID
            university_result = self.supabase.table('universities').select('*').eq('university_id',
                                                                                   university_id).execute()
            if not university_result.data:
                return None  # University not found

            university = Universities(**university_result.data[0])

            # Fetch all students enrolled in the university
            students_result = self.supabase.table('student').select('*').eq('university_id', university_id).execute()
            students = [Student(**student) for student in students_result.data]

            # Fetch grades for each student (if students exist)
            students_with_grades = []
            if students:
                for student in students:
                    grades_result = self.supabase.table('grades').select('*').eq('student_id', student.id).execute()
                    grades = [Grade(**grade) for grade in grades_result.data]
                    students_with_grades.append({
                        "student": student.__dict__,
                        "grades": [grade.__dict__ for grade in grades]
                    })

            # Fetch all majors offered by the university, including maxCapacity and minimumScore
            majors_result = self.supabase.table('university_major') \
                .select('major_id, maxcapacity, minimumscore') \
                .eq('university_id', university_id) \
                .execute()

            majors = []
            for row in majors_result.data:
                major_id = row['major_id']
                max_capacity = row['maxcapacity']
                minimum_score = row['minimumscore']

                # Fetch major details from the majors table
                major_result = self.supabase.table('majors').select('*').eq('major_id', major_id).execute()
                if major_result.data:
                    major = Major(**major_result.data[0])
                    majors.append({
                        "major_id": major.major_id,
                        "name": major.name,
                        "maxCapacity": max_capacity,
                        "minimumScore": minimum_score,
                        "created_at": major.created_at
                    })

            # Combine all data into a single response
            return {
                "university": university.__dict__,
                "students": students_with_grades,
                "majors": majors
            }
        except Exception as e:
            print(f"Error fetching university details: {e}")
            return None