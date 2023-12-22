# app/__init__.py
from flask import Flask, request
from .models import db
from .controllers import create_user, get_user_tasks, create_user_task, delete_user_task, update_user_task


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.before_request
    def disable_authentication():
        if request.method == 'DELETE':
            return
        pass

    return app


app = create_app()
