from flask import Flask
# from app.routes.admin import admin_bp
from app.routes.university import university_bp
from app.routes.student import student_bp
from app.routes.major import major_bp
from app.routes.activity import activity_bp
from app.routes.admin import admin_bp
from app.routes.student_activity import student_activity_bp
from app.routes.grade import grade_bp


from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprint
    app.register_blueprint(university_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(major_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_activity_bp)
    app.register_blueprint(grade_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)