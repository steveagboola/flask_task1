from app import app
from fake_data.tasks import tasks_list


# Checking to see if my route works:  flask --debug run
@app.route("/")
def hello_world():
    first_name = "Steve"
    last_name = "Agboola"
    return f'Hello From: {first_name} {last_name}'

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