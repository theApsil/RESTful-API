from flask import abort, request
from .models import db, User, Todo


def create_user(username):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        abort(400, 'Username already exists')

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()


def get_user_tasks(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404, 'User not found')

    todos = Todo.query.filter_by(user_id=user.id).all()
    tasks = [{'id': todo.id, 'task': todo.task, 'done': todo.done} for todo in todos]
    return tasks


def create_user_task(username, task):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404, 'User not found')

    new_todo = Todo(user_id=user.id, task=task)
    db.session.add(new_todo)
    db.session.commit()




def delete_user_task(task_id):
    todo = Todo.query.get(task_id)
    if not todo:
        abort(404, 'Task not found')

    db.session.delete(todo)
    db.session.commit()


def update_user_task(task_id, data):
    todo = Todo.query.get(task_id)
    if not todo:
        abort(404, 'Task not found')

    if 'task' in data:
        todo.task = data['task']
    if 'done' in data:
        todo.done = data['done']

    db.session.commit()
