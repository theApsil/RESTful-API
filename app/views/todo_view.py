from flask import jsonify


def render_user(user):
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'tasks': [{'task_id': task.task_id, '\ndescription': task.description, '\ncompleted': task.completed} for task in
                  user.tasks]
    })


def render_error(message, status_code):
    return jsonify({'error': message}), status_code
