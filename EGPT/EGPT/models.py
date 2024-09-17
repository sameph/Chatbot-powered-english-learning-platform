from datetime import datetime
from flask import current_app
from EGPT import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    progress = db.relationship('UserProgress', backref='user', lazy=True)
    messages = db.relationship('Messages', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorial.id'), nullable=False)
    is_viewed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"UserProgress(User ID: {self.user_id}, Tutorial ID: {self.tutorial_id}, Viewed: {self.is_viewed})"


class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    video_url = db.Column(db.String(255), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    user_progress = db.relationship('UserProgress', backref='tutorial', lazy=True)

    def __repr__(self):
        return f"Tutorial('{self.title}', '{self.video_url}')"


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    tutorials = db.relationship('Tutorial', backref='service', lazy=True)

    def __repr__(self):
        return f"Service('{self.name}')"


class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return f"word('{self.word}')"
    

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Messages('{self.message}', '{self.timestamp}')"
