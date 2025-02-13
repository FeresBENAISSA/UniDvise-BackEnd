from typing import List

from flask import Blueprint, jsonify, request, abort

from app.models.database import Grade, Activity
from app.services.student_service import StudentService
from app.services.grade_service import GradeService
from app.services.activity_service import ActivityService

student_bp = Blueprint('student', __name__, url_prefix='/api/students')
student_service = StudentService()
grade_service = GradeService();
activity_service = ActivityService();

@student_bp.route('/', methods=['POST'])
async def create_student():
    data = request.get_json()
    if not data or 'first_name' not in data or 'last_name' not in data or 'email' not in data:
        abort(400, description="Invalid request: 'first_name', 'last_name', and 'email' are required")

    student = await student_service.create_student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        date_of_birth=data.get('date_of_birth'),
        password_hash=data.get('password_hash'),
        location=data.get('location'),
        leadership_position=data.get('leadership_position'),
        university_id=data.get('university_id')
    )
    if student:
        return jsonify(student), 201
    else:
        abort(500, description="Failed to create student")

@student_bp.route('/<int:student_id>', methods=['GET'])
async def get_student(student_id: int):
    student = await student_service.get_student_by_id(student_id)
    if student:
        return jsonify(student)
    else:
        abort(404, description="Student not found")

@student_bp.route('/', methods=['GET'])
async def get_all_students():
    students = await student_service.get_all_students()
    return jsonify(students)

@student_bp.route('/<int:student_id>', methods=['PUT'])
async def update_student(student_id: int):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request: No data provided")

    student = await student_service.update_student(
        student_id=student_id,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        date_of_birth=data.get('date_of_birth'),
        location=data.get('location'),
        password_hash=data.get('password_hash'),
        leadership_position=data.get('leadership_position'),
        university_id=data.get('university_id')
    )
    if student:
        return jsonify(student)
    else:
        abort(404, description="Student not found or update failed")

@student_bp.route('/<int:student_id>', methods=['DELETE'])
async def delete_student(student_id: int):
    success = await student_service.delete_student(student_id)
    if success:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        abort(404, description="Student not found")



@student_bp.route('/<int:student_id>/evaluate', methods=['POST'])
async def evaluate_student(student_id: int):
    data = request.get_json()
    if not data or 'majorName' not in data or 'student_activities' not in data:
        abort(400, description="Invalid request: 'majorName' and 'student_activities' are required")

    result = await student_service.evaluate_student(
        student_id=student_id,
        major_name=data['majorName'],
        student_activities=data['student_activities']  # Pass activities from the request
    )

    if 'error' in result:
        abort(500, description=result['error'])
    else:
        return jsonify(result), 200

@student_bp.route('/<int:student_id>/grades', methods=['GET'])
async def get_student_with_grades(student_id: int):
    try:
        # Fetch the student and their grades
        student_with_grades = await  student_service.get_student_with_grades(student_id)

        if student_with_grades:
            return jsonify(student_with_grades), 200
        else:
            abort(404, description="Student not found or no grades available")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

