from app import db
from datetime import datetime, timedelta
import os
import base64
import re
from werkzeug.security import generate_password_hash, check_password_hash

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    due_date = db.Column(db.DateTime)
    # In SQL - user_id INTEGER NOT NULL, FOREIGN KEY(user_id) REFERENCE user(id)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.save()

    # def __repr__(self):
    #     return f"<Task {self.id}|{self.title}>"
    
    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()    


#########################################################################################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs.get("password", ""))


    def __repr__(self):
        return f"<User {self.id}|{self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

    def check_password(self, plain_text_password):
        return check_password_hash(self.password, plain_text_password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "username": self.username,
            "email": self.email
        }
    
    

    # def check_password(self, plain_text_password):
    #     return check_password_hash(self.password, plain_text_password)

    

