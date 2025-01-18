from datetime import datetime
from typing import List, Optional
from app.config import Config
from app.models.database import Student, Grade, Activity


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

    async def evaluate_student(
                self,
                student_id: int,
                grades: List[Grade],
                location: str,
                activities: List[Activity],
                leadership_position: bool,
                major_name : str
        ) -> dict:
            try:
                # Update student's location and leadership position
                update_data = {
                    'location': location,
                    'leadership_position': leadership_position
                }
                self.supabase.table('student').update(update_data).eq('id', student_id).execute()

                # Save grades to the database
                for grade in grades:
                    grade_data = {
                        'student_id': student_id,
                        'course_name': grade.course_name,
                        'grade_value': grade.grade_value,
                        'semester': grade.semester
                    }
                    self.supabase.table('grade').insert(grade_data).execute()

                # Save activities to the database and link them to the student
                for activity in activities:
                    # Save the activity
                    activity_data = {
                        'activity_name': activity.activity_name,
                        'activity_date': activity.activity_date,
                        'description': activity.description
                    }
                    activity_result = self.supabase.table('activity').insert(activity_data).execute()
                    activity_id = activity_result.data[0]['id']

                    # Link the activity to the student
                    student_activity_data = {
                        'student_id': student_id,
                        'activity_id': activity_id
                    }
                    self.supabase.table('student_activity').insert(student_activity_data).execute()
                    # Get all majors with the given name
                    majors_result = self.supabase.table('major').select('university_id').ilike('name',
                                                                                               f'%{major_name}%').execute()
                    university_ids = [major['university_id'] for major in majors_result.data]

                    # Get universities with the filtered IDs
                    universities_result = self.supabase.table('university').select('*').in_('id',
                                                                                            university_ids).execute()




                return {"message": "Student evaluation completed successfully"}
            except Exception as e:
                print(f"Error evaluating student: {e}")
                return {"error": str(e)}