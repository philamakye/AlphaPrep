from app.models import User, User_progress, User_achievement
from flask import render_template, url_for, flash, redirect, request, send_file, session
from flask_login import current_user
from app.extensions import db, mail
import os
import secrets
#from PIL import Image
from flask_mail import Message

from flask import current_app as app


user = current_user

def send_email(to, subject, template):  # remember the send email at the registration route? Yeah ein this. Read on flask mails chale you'll be fine
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=('Alpha Prep', 'noreply@sender.com')
    )
    mail.send(msg)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=('Alpha Prep', 'noreply@sender.com'), recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email and no changes would be made
    '''
    mail.send(msg)  

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    
#    output_size = (125, 125) #minimizing the size of the image so it isn't saved so large in the database
#    i = Image.open(form_picture)
#    i.thumbnail(output_size)
#    i.save(picture_path)

    
    return picture_fn


#  after level 3 it'll revert to level 1, so set the parameters for setting everything back to 0 *evil smile*

def level_checker(user): # checks the level of the user and commits any changes to the database
    subject_level = user.subject_level[-1]
    achievement = user.user_achievement[-1]
    
    
    
    if user.english_points >= 500 and user.english_points < 1500:
        subject_level.english_level = 2
    
    elif user.english_points >= 1500:
        subject_level.english_level = 3   
    else:
        subject_level.english_level = 1
        
        
    if user.social_points >= 500 and user.social_points < 1500:
        subject_level.social_level = 2
        
    
    elif user.social_points >= 1500:
        subject_level.social_level = 3   
    else:
        subject_level.social_level = 1
     
     
    if user.inter_points >= 500 and user.inter_points < 1500:
        subject_level.inter_level = 2
    
    elif user.inter_points >= 1500:
        subject_level.inter_level = 3  
    else:
        subject_level.inter_level = 1  
      
      
    if user.math_points >= 500 and user.social_points < 1500:
        subject_level.math_level = 2
    
    elif user.math_points >= 1500:
        subject_level.math_level = 3  
    else:
        subject_level.math_level = 1     
    
    
    
    user.user_points = user.user_streak[-1].streak_points + user.english_points + user.math_points + user.social_points + user.inter_points
    
    current_points = user.user_points # temporal variable to hold current points of user
    user.user_level = (subject_level.math_level + subject_level.inter_level + subject_level.social_level + subject_level.english_level) // 4
    
    
    if current_points>= 100 and current_points<= 200:
        achievement.crowns = 1
    elif current_points > 200 and current_points <= 300:
        achievement.crowns = 2
    elif current_points > 300 and current_points <= 650:
        achievement.crowns = 3
    elif current_points > 650 and current_points <= 900:
        achievement.crowns = 4
    elif current_points > 900 and current_points <= 1150:
        achievement.crowns = 5
    elif current_points > 1150 and current_points <= 1400:
        achievement.crowns = 6
        
    else:
        if current_points < 100:
            achievement.crowns = 0
    
    
    
    
    if user.user_level == 2:
        flag = 1
        achievement.trophies = "Silver"
    elif user.user_level == 3:
        flag = 2
        achievement.trophies = "Gold"
        
    else:
        flag = 0
        achievement.trophies = "None"
    db.session.add(achievement)
    db.session.commit()    
    
    return user.user_level, flag
    
    
    # this function is meant to cap user points for certain subjects at a certain level
    # add an extra if for when users send two courses over a certain threshold leaving the last one 
  


def streak_checker(login_time, last_login):
    if (login_time.day - last_login.day) == 1:
        
        streak = user.user_streak[-1]
        streak.current_streak += 1
        point_adder = 1
        if streak.longest_streak < streak.current_streak:
            streak.longest_streak += 1
        flash = 0    
     
    elif (login_time.day - last_login.day) == 0:
        streak = user.user_streak[-1]
        point_adder = 0
        flash = 1
    else:
        streak = user.user_streak[-1]
        point_adder =  0
        streak.current_streak = 0
        flash = 2

    return streak.current_streak, streak.longest_streak, point_adder, flash



def sort_by(sort,view, page, per_page):
    if sort != 'all':
        if view == 'highest':
            sorted = User_progress.query.filter_by(author=user, last_subject=sort)\
            .order_by(User_progress.last_score.desc())\
            .paginate(page=page, per_page=per_page)
          
                
        elif view == 'lowest':
            sorted = User_progress.query.filter_by(author=user, last_subject=sort)\
            .order_by(User_progress.last_score.asc())\
            .paginate(page=page, per_page=per_page)
                
        elif  view == 'recent':
            sorted = User_progress.query.filter_by(author=user, last_subject=sort)\
            .order_by(User_progress.date_taken.desc())\
            .paginate(page=page, per_page=per_page)
            
        elif  view == 'oldest':
            sorted = User_progress.query.filter_by(author=user, last_subject=sort)\
            .order_by(User_progress.date_taken.asc())\
            .paginate(page=page, per_page=per_page)    
            
    else:
        if view == 'highest':
            sorted = User_progress.query.filter_by(author=user)\
            .order_by(User_progress.last_score.desc())\
            .paginate(page=page, per_page=per_page)
          
                
        elif view == 'lowest':
            sorted = User_progress.query.filter_by(author=user)\
            .order_by(User_progress.last_score.asc())\
            .paginate(page=page, per_page=per_page)
                
        elif  view == 'recent':
            sorted = User_progress.query.filter_by(author=user)\
            .order_by(User_progress.date_taken.desc())\
            .paginate(page=page, per_page=per_page)
            
        elif  view == 'oldest':
            sorted = User_progress.query.filter_by(author=user)\
            .order_by(User_progress.date_taken.asc())\
            .paginate(page=page, per_page=per_page)
            
            
            
    return sorted