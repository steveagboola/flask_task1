from flask import request
from app import app, db
from datetime import datetime
# from fake_data.tasks import tasks_list
from app.models import Task, User
from app.auth import basic_auth, token_auth



#Checking to see if my route works:  flask --debug run
@app.route("/")
def hello_world():
    first_name = "Steve"
    last_name = "Agboola"
    return f'Hello From: {first_name} {last_name}'

# USER ENDPOINTS 
@app.route("/token")
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return {"token":token,
            "tokenExpiration":user.token_expiration}

##########################################################################

# TASK

# (Retrieve) Get all tasks
@app.route('/tasks')
def get_task():
    # Get the task from the database
    task = db.session.execute(db.select(Task)).scalars().all()
    # return a list of the dictionary version of each t in task
    return [t.to_dict() for t in task]


# (Retrieve) Now get a single task by its ID 
@app.route('/tasks/<int:task_id>')
def get_task_by_id(task_id):
    # Getting task data
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f'Task with an ID of {task_id} does not exist'}, 404

# (Create) Creating a new task
@app.route('/tasks', methods=['POST'])
@token_auth.login_required
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
    
    # Get data from the body
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('dueDate') #optional will return none if no dueDate key in request. Not in required field
    
   #get logged in user
    user = token_auth.current_user()

    # Create a new instance of Task which will add to our database
    new_task = Task(title=title, description = description, user_id=user.id)
    return new_task.to_dict(), 201

# (Update)
# Edit Task
@app.route('/tasks/<int:task_id>', methods=["PUT"]) #This this is an update, make sure this is a PUT request and not a POST request.  POST is used for creation
@token_auth.login_required
def edit_post(task_id):
    # check if they sent a good request
    if not request.is_json:
        return {"error":"Your content-type is not application/json"}, 400
    # lets find the task in our db
    task = db.session.get(Task, task_id)
    # if we cant find it, let em know
    if task is None:
        return {"error":f"post with the id of {task_id} does not exist!"}, 404
    # get the token from current user 
    current_user = token_auth.current_user()
    # check and make sure they are the original author or they cant edit
    if task.author is not current_user:
        return {"error":"This is not your post, you cant edit this"}, 403
    # then they can get the green light
    data = request.json
    task.update(**data)
    return task.to_dict()


#delete

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@token_auth.login_required
def delete_post(task_id):
    # get the post
    task = db.session.get(Task, task_id)
    # check if it exists
    if task is None:
        return {"error":f"We cannot locate posts with the id of {task_id}"}, 404
    # get the logged in user token
    current_user = token_auth.current_user()
    # check to make sure the logged in user is post author
    if task.author is not current_user:
        return {"error":"You can do that, this sint your post! Get outta here!"}, 403
    # delete post
    task.delete()
    return {"success":f"{task.title} has been deleted!"}


#############################################################################################
#User

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

#update
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def edit_user(user_id):
    # check if they sent the data correctly
    if not request.is_json:
        return {"error": "your content type must be application/json !"}, 400
    # get user based off id
    user = db.session.get(User, user_id)
    # make sure it exists
    if user is None:
        return {"error": f"User with {user_id} does not exist"},404
    # get their token
    current_user = token_auth.current_user()
    # make sure they are the person logged in
    if user is not current_user:
        return {"error":"You cannot change this user as you are not them!"} ,403
    # then we update!
    data = request.json
    user.update(**data)
    return user.to_dict()


#delete
@app.route("/users/<int:user_id>", methods=["DELETE"])
@token_auth.login_required
def delete_user(user_id):
    # get the user based on the id
    user = db.session.get(User, user_id)
    #get token
    current_user = token_auth.current_user()
    # make sure its a real user
    if user is None:
        return {"error":f"User with {user_id} not found!"},404
    # make sure user to del is current user
    if user is not current_user:
        return {"error":"You cant do that, delete yourself only"}, 403
    # delete the user 
    user.delete()
    return{"success":f"{user.username} has been deleted!"}


#retrieve? 
@app.get("/users/<int:user_id>")
def get_user(user_id):
    #get the user
    user = db.session.get(User, user_id)
    #if no user let them know
    if user:
        return user.to_dict()
    else:
        return {"error":f" user with id:{user_id} not found"}, 404


