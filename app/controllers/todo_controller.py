from flask import Flask, request, jsonify
from user import User
from task import Task

app = Flask(__name__)

users = [
    User(user_id=1, username="user1"),
    User(user_id=2, username="user2"),
]

# Dummy data
users[0].tasks = [Task(task_id=1, description="Task 1"), Task(task_id=2, description="Task 2")]
users[1].tasks = [Task(task_id=3, description="Task 3")]


def get_user_by_id(user_id):
    for user in users:
        if user.user_id == user_id:
            return user
    return None


@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = len(users) + 1
    username = data.get('username')
    new_user = User(user_id=user_id, username=username)
    users.append(new_user)
    return jsonify({'user_id': new_user.user_id, 'username': new_user.username}), 201


@app.route('/todo', methods=['GET'])
def get_user_tasks():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    tasks = [{'task_id': task.task_id, 'description': task.description, 'completed': task.completed} for task in
             user.tasks]
    return jsonify({'user_id': user.user_id, 'username': user.username, 'tasks': tasks})


@app.route('/todo', methods=['POST'])
def add_task():
    data = request.get_json()
    user_id = data.get('user_id')
    description = data.get('description')

    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    task_id = len(user.tasks) + 1
    new_task = Task(task_id=task_id, description=description)
    user.tasks.append(new_task)

    return jsonify(
        {'task_id': new_task.task_id, 'description': new_task.description, 'completed': new_task.completed}), 201


@app.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    tasks = user.tasks
    for task in tasks:
        if task.task_id == task_id:
            tasks.remove(task)
            return jsonify({'message': 'Task deleted successfully'}), 200

    return jsonify({'error': 'Task not found'}), 404


@app.route('/todo/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user = get_user_by_id(int(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    for task in user.tasks:
        if task.task_id == task_id:
            task.description = data.get('description', task.description)
            task.completed = data.get('completed', task.completed)
            return jsonify({'task_id': task.task_id, 'description': task.description, 'completed': task.completed}), 200

    return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
