from flask import Blueprint, jsonify, request, abort
from app.services.student_activity_service import StudentActivityService

student_activity_bp = Blueprint('student_activity', __name__, url_prefix='/api/student-activities')
student_activity_service = StudentActivityService()

@student_activity_bp.route('/', methods=['POST'])
async def create_student_activity():
    data = request.get_json()
    if not data or 'student_id' not in data or 'activity_id' not in data:
        abort(400, description="Invalid request: 'student_id' and 'activity_id' are required")

    student_activity = await student_activity_service.create_student_activity(
        student_id=data['student_id'],
        activity_id=data['activity_id']
    )
    if student_activity:
        return jsonify(student_activity), 201
    else:
        abort(500, description="Failed to create sytudent activit")

@student_activity_bp.route('/<int:student_id>/<int:activity_id>', methods=['GET'])
async def get_student_activity(student_id: int, activity_id: int):
    student_activity = await student_activity_service.get_student_activity_by_id(student_id, activity_id)
    if student_activity:
        return jsonify(student_activity)
    else:
        abort(404, description="Student activity not found")

@student_activity_bp.route('/', methods=['GET'])
async def get_all_student_activities():
    student_activities = await student_activity_service.get_all_student_activities()
    return jsonify(student_activities)

@student_activity_bp.route('/<int:student_id>/<int:activity_id>', methods=['DELETE'])
async def delete_student_activity(student_id: int, activity_id: int):
    success = await student_activity_service.delete_student_activity(student_id, activity_id)
    if success:
        return jsonify({"message": "Student activity deleted successfully"}), 200
    else:
        abort(404, description="Student activity not found")





# Both cases student exist in database - new ws all payload save in the database +
# INPUT:
#    Grades: -> student -> student id
#    Location -> student -> student id
#    Activites -> student -> student id
#    LeaderShipPosition  -> student -> student id

#      100 Universite => filter by Major => 30 Universite => Universite Name + minScore + Location
