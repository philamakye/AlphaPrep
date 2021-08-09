from app.extensions import mysql
import random, copy
from app.extensions import db
from app.models import User
from flask_login import current_user
import os



# update all the stuff to allow for different levels
# s = subject, u = usr_lvl, t = topic
def load_questions(s,u,t): # loads questions dependent on the subject 
    if s == 'english':
        mycursor = mysql.connect().cursor()
        mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u) + ' and topic = %s order by rand() limit 5', t) 
        myresult = mycursor.fetchall()
        original_questions = {}
    
        for each in myresult:
            original_questions[each[0]] = [each[1:]]
    

        questions = copy.deepcopy(original_questions)
    
    else:
        if u == 1:
            mycursor = mysql.connect().cursor()
            mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u) + ' order by rand() limit 20') 
            myresult = mycursor.fetchall()
            
        if u == 2:
            mycursor = mysql.connect().cursor()
            mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u-1) + ' order by rand() limit 5') 
            myresult1 = mycursor.fetchall()
            mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u) + ' order by rand() limit 15') 
            myresult2 = mycursor.fetchall()
            myresult = myresult1 + myresult2
            
        if u ==3:
            mycursor = mysql.connect().cursor()
            mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u-2) + ' order by rand() limit 2') 
            myresult1 = mycursor.fetchall()
            mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u-1) + ' order by rand() limit 3') 
            myresult2 = mycursor.fetchall()
            mycursor.execute('select question, option_a, option_b, option_c, option_d from ' + str(s) + ' where usr_lvl= ' + str(u) + ' order by rand() limit 15') 
            myresult3 = mycursor.fetchall()
            myresult = myresult1 + myresult2 + myresult3
            
        
        original_questions = {}
        for each in myresult:
            original_questions[each[0]] = [each[1:]]
    

        questions = copy.deepcopy(original_questions)
    
    
    return questions

def load_answers(s,u,t):
    if s == 'english' :
        mycursor = mysql.connect().cursor()
        mycursor.execute('select question, correct_answer from '  + str(s) + ' where usr_lvl= ' + str(u) + ' and topic = %s', t)
        rere = mycursor.fetchall()
        answers = {}

    
        for each in rere:
            answers[each[0]] = [each[1:]]
            
    else:
        mycursor = mysql.connect().cursor()
        mycursor.execute('select question, correct_answer from '  + str(s) + ' where usr_lvl= ' + str(u))
        rere = mycursor.fetchall()
        answers = {}
        
        for each in rere:
            answers[each[0]] = [each[1:]]
            
    return answers

    
   
   # these following functions load the stories for english, the database for them is different that's why i use these functions
def load_story(t):
    mycursor = mysql.connect().cursor()
    mycursor.execute('Select story from Stories where storyid =%s', t)
    myresult = mycursor.fetchall()
      
        
    return myresult
    
def load_storyoptions(t):
    mycursor = mysql.connect().cursor()
    mycursor.execute('Select qid, option_a, option_b, option_c, option_d from StoryOptions where storyid =%s ', t)
    myresult1 = mycursor.fetchall()
    options = {}
        
    for each in myresult1:
        options[each[0]] = [each[1:]]
        
    optionss = copy.deepcopy(options)
    
    
    return optionss
    
def load_storyanswers(t):
    mycursor = mysql.connect().cursor()
    mycursor.execute('Select qid, correct_answer from StoryOptions where storyid =%s ', t)
    myresult1 = mycursor.fetchall()
    options = {}
    for each in myresult1:
        options[each[0]] = [each[1:]]
    
    return options


def load_videos(s, t):
    mycursor = mysql.connect().cursor()
    mycursor.execute('Select link from ' + str(s) +'_videos where topic = %s ', t)
    myresult1 = mycursor.fetchall()
   
    
    return myresult1   
    

    
def load_pdfs(s, t):
    if s != 'math':
        mycursor = mysql.connect().cursor()
        mycursor.execute('Select link from ' + str(s) +'_pdf where topic=%s ', t)
        myresult1 = mycursor.fetchall()
    else:
        mycursor = mysql.connect().cursor()
        mycursor.execute('Select link from ' + str(s) +'_pdf')
        myresult1 = mycursor.fetchall()
        
    return myresult1
    
    # takes the subject and the correct answer
    # this function to fetch the topic won't work for my current database, but it would with the updated database
def load_topic(s,c):
    mycursor = mysql.connect().cursor()
    mycursor.execute('Select topic from ' + str(s) + ' where correct_answer =%s ', c) 
    myresult1 = mycursor.fetchall()
    options = {}
        
    for each in myresult1:
        options[each[0]] = [each[1:]]
        
    optionss = copy.deepcopy(options)
    
    return myresult1
    
    
def load_bug_report(report):
    mycursor = mysql.connect().cursor()
    mycursor.execute(' INSERT INTO bug_report (report)  VALUES (%s) ', report)
    