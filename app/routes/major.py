from flask import Blueprint, jsonify, request, abort
from app.services.major_service import MajorService

major_bp = Blueprint('major', __name__, url_prefix='/api/majors')
major_service = MajorService()

# Create a new major
@major_bp.route('/', methods=['POST'])
async def create_major():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            abort(400, description="Invalid request: 'name' is required")

        major = await major_service.create_major(
            name=data['name'],
            university_id=data.get('university_id')
        )
        if major:
            return jsonify(major), 201
        else:
            abort(500, description="Failed to create major")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Get all majors
@major_bp.route('/', methods=['GET'])
async def get_all_majors():
    try:
        majors = await major_service.get_all_majors()
        return jsonify(majors)
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Get a specific major by ID
@major_bp.route('/<int:major_id>', methods=['GET'])
async def get_major(major_id: int):
    try:
        major = await major_service.get_major_by_id(major_id)
        if major:
            return jsonify(major)
        else:
            abort(404, description="Major not found")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Update a major
@major_bp.route('/<int:major_id>', methods=['PUT'])
async def update_major(major_id: int):
    try:
        data = request.get_json()
        if not data:
            abort(400, description="Invalid request: No data provided")

        major = await major_service.update_major(
            major_id=major_id,
            name=data.get('name'),
            university_id=data.get('university_id')
        )
        if major:
            return jsonify(major)
        else:
            abort(404, description="Major not found or update failed")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Delete a major
@major_bp.route('/<int:major_id>', methods=['DELETE'])
async def delete_major(major_id: int):
    try:
        success = await major_service.delete_major(major_id)
        if success:
            return jsonify({"message": "Major deleted successfully"}), 200
        else:
            abort(404, description="Major not found")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")

# Assign a major to a university
@major_bp.route('/<int:major_id>/assign-university', methods=['POST'])
async def assign_major_to_university(major_id: int):
    try:
        data = request.get_json()
        if not data or 'university_id' not in data:
            abort(400, description="Invalid request: 'university_id' is required")

        university_id = data['university_id']
        updated_major = await major_service.assign_major_to_university(major_id, university_id)

        if updated_major:
            return jsonify(updated_major), 200
        else:
            abort(404, description="Major not found or update failed")
    except Exception as e:
        abort(500, description=f"An error occurred: {str(e)}")