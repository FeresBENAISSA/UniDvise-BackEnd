from flask import Blueprint, jsonify, request, abort
from app.services.major_service import MajorService

major_bp = Blueprint('major', __name__, url_prefix='/api/majors')
major_service = MajorService()

# Create a new major
@major_bp.route('/', methods=['POST'])
def create_major():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            abort(400, description="Invalid request: 'name' is required")

        major = major_service.create_major(
            name=data['name']
        )
        return jsonify(major), 201
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Get all majors
@major_bp.route('/', methods=['GET'])
def get_all_majors():
    try:
        majors = major_service.get_all_majors()
        return jsonify(majors)
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Get a specific major by ID
@major_bp.route('/<int:major_id>', methods=['GET'])
def get_major(major_id: int):
    try:
        major = major_service.get_major_by_id(major_id)
        if major:
            return jsonify(major)
        else:
            abort(404, description="Major not found")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Update a major
@major_bp.route('/<int:major_id>', methods=['PUT'])
def update_major(major_id: int):
    try:
        data = request.get_json()
        if not data:
            abort(400, description="Invalid request: No data provided")

        major = major_service.update_major(
            major_id=major_id,
            name=data.get('name')
        )
        if major:
            return jsonify(major)
        else:
            abort(404, description="Major not found or update failed")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Delete a major
@major_bp.route('/<int:major_id>', methods=['DELETE'])
def delete_major(major_id: int):
    try:
        success = major_service.delete_major(major_id)
        if success:
            return jsonify({"message": "Major deleted successfully"}), 200
        else:
            abort(404, description="Major not found")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Assign a major to a university (via UniversityMajor)
@major_bp.route('/<int:major_id>/assign-university', methods=['POST'])
def assign_major_to_university(major_id: int):
    try:
        data = request.get_json()
        if not data or 'university_id' not in data or 'maxCapacity' not in data or 'minimumScore' not in data:
            abort(400, description="Invalid request: 'university_id', 'maxCapacity', and 'minimumScore' are required")

        university_id = data['university_id']
        max_capacity = data['maxCapacity']
        minimum_score = data['minimumScore']

        university_major = major_service.assign_major_to_university(
            major_id=major_id,
            university_id=university_id,
            max_capacity=max_capacity,
            minimum_score=minimum_score
        )
        if university_major:
            return jsonify(university_major), 200
        else:
            abort(404, description="Major or University not found, or assignment failed")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")