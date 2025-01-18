from flask import Blueprint, jsonify, request, abort
from app.services.grade_service import GradeService

grade_bp = Blueprint('grade', __name__, url_prefix='/api/grades')
grade_service = GradeService()

@grade_bp.route('/', methods=['POST'])
async def create_grade():
    data = request.get_json()
    if not data or 'student_id' not in data or 'course_name' not in data or 'grade_value' not in data:
        abort(400, description="Invalid request: 'student_id', 'course_name', and 'grade_value' are required")

    grade = await grade_service.create_grade(
        student_id=data['student_id'],
        course_name=data['course_name'],
        grade_value=data['grade_value'],
        semester=data.get('semester')
    )
    if grade:
        return jsonify(grade), 201
    else:
        abort(500, description="Failed to create grade")

@grade_bp.route('/<int:grade_id>', methods=['GET'])
async def get_grade(grade_id: int):
    grade = await grade_service.get_grade_by_id(grade_id)
    if grade:
        return jsonify(grade)
    else:
        abort(404, description="Grade not found")

@grade_bp.route('/', methods=['GET'])
async def get_all_grades():
    grades = await grade_service.get_all_grades()
    return jsonify(grades)

@grade_bp.route('/<int:grade_id>', methods=['PUT'])
async def update_grade(grade_id: int):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request: No data provided")

    grade = await grade_service.update_grade(
        grade_id=grade_id,
        course_name=data.get('course_name'),
        grade_value=data.get('grade_value'),
        semester=data.get('semester')
    )
    if grade:
        return jsonify(grade)
    else:
        abort(404, description="Grade not found or update failed")

@grade_bp.route('/<int:grade_id>', methods=['DELETE'])
async def delete_grade(grade_id: int):
    success = await grade_service.delete_grade(grade_id)
    if success:
        return jsonify({"message": "Grade deleted successfully"}), 200
    else:
        abort(404, description="Grade not found")