from flask import Blueprint, jsonify, request, abort
from app.services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admins')
admin_service = AdminService()

@admin_bp.route('/', methods=['POST'])
async def create_admin():
    data = request.get_json()
    if not data or 'username' not in data or 'password_hash' not in data or 'email' not in data:
        abort(400, description="Invalid request: 'username', 'password_hash', and 'email' are required")

    admin = await admin_service.create_admin(
        username=data['username'],
        password_hash=data['password_hash'],
        email=data['email']
    )
    if admin:
        return jsonify(admin), 201
    else:
        abort(500, description="Failed to create admin")

@admin_bp.route('/<int:admin_id>', methods=['GET'])
async def get_admin(admin_id: int):
    admin = await admin_service.get_admin_by_id(admin_id)
    if admin:
        return jsonify(admin)
    else:
        abort(404, description="Admin not found")

@admin_bp.route('/', methods=['GET'])
async def get_all_admins():
    admins = await admin_service.get_all_admins()
    return jsonify(admins)

@admin_bp.route('/<int:admin_id>', methods=['PUT'])
async def update_admin(admin_id: int):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request: No data provided")

    admin = await admin_service.update_admin(
        admin_id=admin_id,
        username=data.get('username'),
        email=data.get('email')
    )
    if admin:
        return jsonify(admin)
    else:
        abort(404, description="Admin not found or update failed")

@admin_bp.route('/<int:admin_id>', methods=['DELETE'])
async def delete_admin(admin_id: int):
    success = await admin_service.delete_admin(admin_id)
    if success:
        return jsonify({"message": "Admin deleted successfully"}), 200
    else:
        abort(404, description="Admin not found")