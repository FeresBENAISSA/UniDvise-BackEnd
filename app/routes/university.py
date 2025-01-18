from flask import Blueprint, jsonify, request, abort
from app.services.university_service import UniversityService

# Create a blueprint with the base route '/api/universities'
university_bp = Blueprint('university', __name__, url_prefix='/api/universities')
university_service = UniversityService()

# Get all universities
@university_bp.route('/', methods=['GET'])
def get_all_universities():
    try:
        universities = university_service.get_all_universities()
        return jsonify([university.__dict__ for university in universities])
    except Exception as e:
        abort(500, description=f"An error occurred while fetching universities: {str(e)}")

# Get a specific university by ID
@university_bp.route('/<int:university_id>', methods=['GET'])
def get_university(university_id: int):
    try:
        university = university_service.get_university_by_id(university_id)
        if university:
            return jsonify(university.__dict__)
        else:
            abort(404, description="University not found")
    except Exception as e:
        abort(500, description=f"An error occurred while fetching the university: {str(e)}")

# Create a new university
@university_bp.route('/', methods=['POST'])
def create_university():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            abort(400, description="Invalid request: 'name' is required")

        university = university_service.create_university(
            name=data['name'],
            location=data.get('location'),
            minscore=data.get('minscore'),
            admin_id=data.get('admin_id')
        )
        if university:
            return jsonify(university.__dict__), 201
        else:
            abort(500, description="Failed to create university")
    except Exception as e:
        abort(500, description=f"An error occurred while creating the university: {str(e)}")

# Get all students for a specific university
@university_bp.route('/<int:university_id>/students', methods=['GET'])
def get_university_students(university_id: int):
    try:
        students = university_service.get_university_students(university_id)
        return jsonify([student.__dict__ for student in students])
    except Exception as e:
        abort(500, description=f"An error occurred while fetching students: {str(e)}")

# Get all majors for a specific university
@university_bp.route('/<int:university_id>/majors', methods=['GET'])
def get_university_majors(university_id: int):
    try:
        majors = university_service.get_university_majors(university_id)
        return jsonify([major.__dict__ for major in majors])
    except Exception as e:
        abort(500, description=f"An error occurred while fetching majors: {str(e)}")

# Get all activities for a specific university
@university_bp.route('/<int:university_id>/activities', methods=['GET'])
def get_university_activities(university_id: int):
    try:
        activities = university_service.get_university_activities(university_id)
        return jsonify([activity.__dict__ for activity in activities])
    except Exception as e:
        abort(500, description=f"An error occurred while fetching activities: {str(e)}")

# Get all grades for a specific university
@university_bp.route('/<int:university_id>/grades', methods=['GET'])
def get_university_grades(university_id: int):
    try:
        grades = university_service.get_university_grades(university_id)
        return jsonify([grade.__dict__ for grade in grades])
    except Exception as e:
        abort(500, description=f"An error occurred while fetching grades: {str(e)}")