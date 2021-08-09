from .extensions import db, login_manager
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from flask import current_app as app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,  primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable = False)
    course = db.Column(db.String(20), nullable = False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    user_progress = db.relationship('User_progress', backref='author', lazy=True)
    user_streak = db.relationship('User_streak', backref = 'author', lazy=True)
    user_achievement = db.relationship('User_achievement', backref='author', lazy=True)
    user_level = db.Column(db.Integer, nullable = False, default = 1)
    subject_level = db.relationship('Subject_level', backref = 'author', lazy=True)
    user_points = db.Column(db.Integer, nullable = False, default = 0)
    english_points = db.Column(db.Integer, nullable = False, default = 0)
    inter_points = db.Column(db.Integer, nullable = False, default = 0)
    social_points = db.Column(db.Integer, nullable = False, default = 0)
    math_points = db.Column(db.Integer, nullable = False, default = 0)
    
    
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod 
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
    
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.user_level}', '{self.user_points}', '{self.english_points}', '{self.inter_points}', '{self.social_points}')"
    


    
class User_progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_subject= db.Column(db.String(100), default="N/A")
    last_score = db.Column(db.Integer, default=0)
    date_taken = db.Column(db.DateTime, nullable= False, default=datetime.utcnow)
    last_recommendation = db.Column(db.String(1000), default="N/A")
    
    
    
    def __repr__(self):
        return f"User('{self.last_subject}', '{self.last_score}', '{self.date_taken}', '{self.last_recommendation}')"
        


class User_streak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    streak_points = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime,  default=datetime.utcnow )
    
    
    def __repr__(self):
        return f"User('{self.user}', '{self.current_streak}', '{self.longest_streak}')"
        
        
class Subject_level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    math_level = db.Column(db.Integer, default=1)
    english_level = db.Column(db.Integer, default=1)
    social_level = db.Column(db.Integer, default=1)
    inter_level = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f"User('{self.user}', '{self.math_level}', '{self.english_level}', '{self.social_level}', '{self.inter_level}')"
        

class User_achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crowns = db.Column(db.Integer, default=0)
    trophies = db.Column(db.String(20), nullable = False, default="None")
    
    def __repr__(self):
        return f"User('{self.user}', '{self.crowns}', '{self.trophies}')"

    
class English(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    usr_lvl = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

    
class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    usr_lvl = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    

class Inter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    usr_lvl = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

    
class Math(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255), nullable=False)
    usr_lvl = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)

    
class Story(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    story = db.Column(db.Text, nullable=False)
    storyoptions = db.relationship('StoryOptions', backref='author', lazy=True)
    
    
class StoryOptions(db.Model):
    __tablename__ = 'storyoptions'
    
    storyid = db.Column(db.String(6), db.ForeignKey('story.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    
