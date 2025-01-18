from flask import Blueprint, jsonify, request, abort
from app.services.activity_service import ActivityService

activity_bp = Blueprint('activity', __name__, url_prefix='/api/activities')
activity_service = ActivityService()

@activity_bp.route('/', methods=['POST'])
async def create_activity():
    data = request.get_json()
    if not data or 'activity_name' not in data:
        abort(400, description="Invalid request: 'activity_name' is required")

    activity = await activity_service.create_activity(
        activity_name=data['activity_name'],
        activity_date=data.get('activity_date'),
        description=data.get('description')
    )
    if activity:
        return jsonify(activity), 201
    else:
        abort(500, description="Failed to create activity")

@activity_bp.route('/<int:activity_id>', methods=['GET'])
async def get_activity(activity_id: int):
    activity = await activity_service.get_activity_by_id(activity_id)
    if activity:
        return jsonify(activity)
    else:
        abort(404, description="Activity not found")

@activity_bp.route('/', methods=['GET'])
async def get_all_activities():
    activities = await activity_service.get_all_activities()
    return jsonify(activities)

@activity_bp.route('/<int:activity_id>', methods=['PUT'])
async def update_activity(activity_id: int):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request: No data provided")

    activity = await activity_service.update_activity(
        activity_id=activity_id,
        activity_name=data.get('activity_name'),
        activity_date=data.get('activity_date'),
        description=data.get('description')
    )
    if activity:
        return jsonify(activity)
    else:
        abort(404, description="Activity not found or update failed")

@activity_bp.route('/<int:activity_id>', methods=['DELETE'])
async def delete_activity(activity_id: int):
    success = await activity_service.delete_activity(activity_id)
    if success:
        return jsonify({"message": "Activity deleted successfully"}), 200
    else:
        abort(404, description="Activity not found")