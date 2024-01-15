from flask import request
from datetime import datetime
from app import app, db
from fake_data.tasks import tasks_list
from app.models import Task, User


# Checking to see if my route works:  flask --debug run
# @app.route("/")
# def hello_world():
#     first_name = "Steve"
#     last_name = "Agboola"
#     return f'Hello From: {first_name} {last_name}'

# Create a route to get the task form fake_data folder
@app.route('/tasks')
def get_tasks():
    # Get task_data
    tasks = tasks_list
    return tasks

# Now get a single task by its ID
@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    # Getting task data
    tasks = tasks_list
    for task in tasks:
        # Check the 'id' key of the task to see if it matches the task_id from URL
        if task['id'] == task_id:
            return task
    return {'error': f'Task with ID {task_id} does not exist'}, 404

# Creating a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'You content-type must be application/json'}, 400
    # Get the data from the request
    data = request.json
    # Check that the data has the required fields
    required_fields = ['title', 'description']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    # Get the values from the request data
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('dueDate') #optional will return none if no dueDate key in request. Not in required field
    # Create the new task withe above values
    new_task = {
        "id": len(tasks_list) + 1,
        "title": title,
        "description": description,
        "completed": False,
        "createdAt": datetime.utcnow(),
        "dueDate": due_date
    }
    # Add the new task to the task_list
    tasks_list.append(new_task)
    return new_task, "201"

#############################################################################################

# Create New User
@app.route('/users', methods=['POST'])
def create_user():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    # Get the data from the request body
    data = request.json

    # Validate that the data has all of the required fields
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get the values from the data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check to see if any current users already have that username and/or email
    check_users = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    # If the list is not empty then someone already has that username or email
    if check_users:
        return {'error': 'A user with that username and/or email already exists'}, 400

    # Create a new user instance with the request data which will add it to the database
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    return new_user.to_dict(), 201