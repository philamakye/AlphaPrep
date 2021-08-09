from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.decorators import check_confirmed
from app.util.quiz import shuffle
from app.util import fxns
import random
from collections import Counter
from app.models import User, Math, English, Social, Inter, Story, StoryOptions


tests = Blueprint(
'tests',
__name__,
static_folder = 'static',
template_folder = 'templates',
static_url_path = '/tests'
)



@tests.route("/english", methods = ['GET', 'POST'])
def english():
    global subject
    subject = 'english'
    if current_user.is_anonymous:
        current_user.user_level = 1

    global sessions
    sessions = 1
    
    global question1
    question1 = dbloader.load_questions('english', current_user.user_level,'opposite in meaning')
    global answer1
    answer1 = dbloader.load_answers('english',current_user.user_level, 'opposite in meaning')
    
    
    global questions_shuffle1
    questions_shuffle1 = shuffle(question1)
    
    global question2
    question2 = dbloader.load_questions('english', current_user.user_level,'best completes')
    global answer2
    answer2 = dbloader.load_answers('english',current_user.user_level, 'best completes')
    
  
    global questions_shuffle2
    questions_shuffle2 = shuffle(question2)
    
    global question4
    question4 = dbloader.load_questions('english', current_user.user_level,'synonyms')
    global answer4
    answer4 = dbloader.load_answers('english',current_user.user_level, 'synonyms')
    
    
    
    global questions_shuffle4
    questions_shuffle4 = shuffle(question4)
    
    global question5
    question5 = dbloader.load_questions('english', current_user.user_level,'interpretations')
    global answer5
    answer5 = dbloader.load_answers('english',current_user.user_level, 'interpretations')
       
    global questions_shuffle5
    questions_shuffle5 = shuffle(question5)
    
    
    global question6
    question6 = dbloader.load_questions('english', current_user.user_level,'literature')
    global answer6
    answer6 = dbloader.load_answers('english',current_user.user_level, 'literature')
    
    global questions_shuffle6
    questions_shuffle6 = shuffle(question6)
    
    
    t = 'st' + str(random.randint(1,15))
    global story
    story = dbloader.load_story(t)
    global optionss
    optionss = dbloader.load_storyoptions(t)
    
    global storyanswers
    storyanswers = dbloader.load_storyanswers(t)
    
    
    return render_template('english.html', title='Test')
    
    
    
@tests.route("/TestLanding", methods = ['GET', 'POST'])
def other_subjects():
    if current_user.is_anonymous:
        current_user.user_level = 1
    
    global subject
    subject = request.form['subject'] # this is how we tell the subject that the user selects
    # loading questions for the other subjects
   
    global sessions
    sessions = 1
    
    global question1
    question1 = dbloader.load_questions(subject, current_user.user_level,('level'+ str(current_user.user_level))) 
    # the level here is redundant but we need it for loading english
    
    
    global answer1
    answer1 = dbloader.load_answers(subject, current_user.user_level, ('level'+ str(current_user.user_level)))
    
    
    global questions_shuffle1
    questions_shuffle1 = shuffle(question1)
    

    return render_template('others.html', title='Test', subject=subject)



sessions = 0 # stops quiz from reloading points into database
@tests.route("/testpage",  methods =['GET', 'POST'])
def page1(): 
    global sessions
    if sessions == 1:
        if subject == 'english':
            global question1
            questions = question1
 
            global questions_shuffle1
            questions_shuffled = questions_shuffle1
        
            global question2
            questions2 = question2
            global questions_shuffle2
            questions_shuffled2 = questions_shuffle2
            
            global story
            t = story
            
            global optionss
            pp = optionss
            
            global question4
            questions4 = question4
            global questions_shuffle4
            questions_shuffled4 = questions_shuffle4
            
            global question5
            questions5 = question5
            global questions_shuffle5
            questions_shuffled5 = questions_shuffle5
            
            global question6
            questions6 = question6
            global questions_shuffle6
            questions_shuffled6 = questions_shuffle6

        
            global correct
            correct = 0
        
            return render_template('testpage.html', q = questions_shuffled, o = questions, p = questions2, q2 = questions_shuffled2, subject = subject, t = story, pp = optionss,
            questions4=questions4, questions_shuffled4=questions_shuffled4, questions5=questions5, questions_shuffled5=questions_shuffled5, questions6=questions6, questions_shuffled6=questions_shuffled6)
        
        else:
            
            questions = question1
            
            questions_shuffled = questions_shuffle1
            
            
            mid = len(questions_shuffled)//2
            
            page_1 = questions_shuffled[:mid]
            page_2 = questions_shuffled[mid:]
            
            
            return render_template('testpage.html',  q = questions_shuffled, o = questions, subject = subject, p1= page_1, p2 = page_2)



@tests.route("/resultspage", methods=['GET', 'POST'])
def resultspage():
    if current_user.is_anonymous:
        current_user.user_level = 1
        
    global subject
    
    global correct
    correct = 0
    correct1=0
    correct2=0
    correct3=0
    correct4=0
    correct5=0
    correct6=0
    global total
    total = 0
    total1 = 0
    total2= 0
    total3= 0
    total4=0
    total5=0
    total6=0
    if subject == 'english':
        
    
        for i in question1.keys():
            total1 += 1
            global answered1
            answered1 = request.form.getlist(i) #gets the answers from the other page
            global bans1
            bans1 = request.form.to_dict(i) # transfers all the answers to a dict, it comes as key: the questions and value: the answers picked
            for j in answer1[i]: #loop for making the work
                if j[0] in answered1:
                    correct1 +=1
        
        global question2
        questions = question2
        global questions_shuffle2
        qt = questions_shuffle2
        wrongs_for_opposites = total1 - correct1
    
        
        global answer2
        answers = answer2
    
        
       
        
        
    
        for i in questions.keys():
            total2 += 1
            global answered2
            answered2 = request.form.getlist(i) #gets the answers from the other page
            global bans2
            bans2 = request.form.to_dict(i) # transfers all the answers to a dict, it comes as key: the questions and value: the answers picked
        
            for j in answers[i]: #loop for making the work
                if j[0] in answered2:
                    correct2 +=1
    
        
        global optionss
        global story
        
        wrongs_for_two = total2 - correct2
        for i in optionss.keys():
            total3 += 1
            global storyanswered
            storyanswered = request.form.getlist(i)
            
            sb = request.form.to_dict(i)
            
            
            
            global storyanswers
            for j in storyanswers[i]:
                if j[0] in storyanswered:
                    correct3 += 1
                    
            
        wrongs_for_three = total3 - correct3
        
        global question4
        questions4 = question4
        global questions_shuffle4
        qt4 = questions_shuffle4
        
        
        
        global answer4
        answers4 = answer4
    
        
        
        
        for i in questions4.keys():
            total4 += 1
            global answered4
            answered4 = request.form.getlist(i) #gets the answers from the other page
            global bans4
            bans4 = request.form.to_dict(i) # transfers all the answers to a dict, it comes as key: the questions and value: the answers picked
            
            for j in answers4[i]: #loop for making the work
                if j[0] in answered4:
                    correct4 +=1
        
        wrongs4 = total4 - correct4 
        
        
        global question5
        questions5 = question5
        global questions_shuffle5
        qt5 = questions_shuffle5
        
    
        
        global answer5
        answers5 = answer5
    
        
        
        
        
        for i in questions5.keys():
            total5 += 1
            global answered5
            answered5 = request.form.getlist(i) #gets the answers from the other page
            global bans5
            bans5 = request.form.to_dict(i) # transfers all the answers to a dict, it comes as key: the questions and value: the answers picked
        
            for j in answers5[i]: #loop for making the work
                if j[0] in answered5:
                    correct5 +=1
        
        
        wrongs5 = total5 - correct5
        
        global question6
        questions6 = question6
        global questions_shuffle6
        qt6 = questions_shuffle6
        
    
        
        global answer6
        answers6 = answer6
    
        
        
        for i in questions6.keys():
            total6 += 1
            global answered6
            answered6 = request.form.getlist(i) #gets the answers from the other page
            global bans6
            bans6 = request.form.to_dict(i) # transfers all the answers to a dict, it comes as key: the questions and value: the answers picked
        
            for j in answers6[i]: #loop for making the work
                if j[0] in answered6:
                    correct6 +=1
        
        
        wrongs6 = total6 - correct6
        
        
        
        wrongs = wrongs_for_opposites + wrongs_for_three + wrongs_for_two + wrongs4 + wrongs5 + wrongs6
        correct = correct1 + correct2 + correct3 + correct4 + correct5 + correct6
        total = total1 + total2 + total3 + total4 + total5 + total6
        global sessions
        
        recommendation_topic = "None"
        
        wrong = [wrongs_for_opposites, wrongs_for_two, wrongs_for_three, wrongs4, wrongs5, wrongs6]
        
        recommendation_index = wrong.index(max(wrong))
        
        count = 0
        
        if max(wrong) / 10 * 100 > 50:
        
            if recommendation_index == 0:
                recommendation = "Opposites"
            elif recommendation_index == 1:
                recommendation = "Best Completes"
            elif recommendation_index == 2:
                recommendation = "Story Problems"
            elif recommendation_index == 3:
                recommendation = "Synonyms"
            elif recommendation_index == 4:
                recommendation = "Best Intepretation"
            elif recommendation_index == 5:
                recommendation = "General Knowledge in Literature"
            else:
                recommendation = "Study everything for your this subject!"
        else:
            recommendation = "None"
            
        
        
        
        if sessions is 1 and current_user.is_authenticated:
           
            current_user.english_points = current_user.english_points + (correct*2) - (wrongs * 0.5)
            
            progress = User_progress(user=current_user.id, last_subject = subject, last_score = correct, last_recommendation=recommendation)
            db.session.add(progress)
            db.session.commit()
            sessions = 0
        
        
            # put the tutorial links somewhere nice, like a variable or database for easy access
        if current_user.is_authenticated:
            level_checker = fxns.level_checker(current_user)
            subject_level = current_user.subject_level[-1]
        else:
            level_checker = 1
            subject_level = 1
                
        if current_user.is_authenticated:
            previous_crowns = current_user.user_achievement[-1].crowns # takes the number of crowns before recalculation
            temp_var = current_user.user_level + 1
            
                
            current_crowns = current_user.user_achievement[-1].crowns
            
            if previous_crowns > current_crowns:
                flash("You lost a crown!", 'success')
            elif previous_crowns < current_crowns:
                flash("You gained a crown!", 'success')
                
            if temp_var == current_user.user_level: # checks if the user has leveled up and the flashes a one time message on their page
                if flashed == 1:
                    flash('You have Leveled Up to Level 2!', 'success')
                    flash("You've gained the Silver Trophy!", 'success')
                elif flashed == 2:
                    flash('You have Leveled Up to Level 3!', 'success')
                    flash("You've gained the Gold Trophy!", 'success')
                    
                    
            
        global temp_subject
        temp_subject = subject
        return render_template('resultspage.html', title='Your Score', correct=correct, subject = subject, q1 = questions_shuffle1, q2 = qt, a1 = answer1, a2 = answer2, b1 = answered1, b2 = answered2, c1 = bans1, c2 = bans2,
        st = story, sa = storyanswers, sb = sb, oo = optionss, wrongs=wrongs, wp=wrongs_for_opposites, wt=wrongs_for_three, wtw=wrongs_for_two, t1=total1, t2 = total2, t3= total3, total=total, r = recommendation,
        q4 = qt4, q5 = qt5, q6 = qt6,a4= answer4, b4=answered4, a5=answer5, b5=answered5, a6=answer6, b6= answered6, w4=wrongs4, w5=wrongs5, w6=wrongs6, t4=total4, t5= total5, t6 = total6,
        c4=bans4, c5=bans5, c6=bans6, correct1=correct1, correct2=correct2, count=count, correct3=correct3, correct4=correct4, correct5=correct5, correct6=correct6, subject_level=subject_level)
    
    
    else: # edit to add recommendation_link for other subjects
        
        others_wrong = 0
        topic = []
        topic_final = []
        
        
        for i in question1.keys():
            total += 1
            answered1 = request.form.getlist(i)
            bans1 = request.form.to_dict(i)
            
            
            for j in answer1[i]:
                if j[0] in answered1:
                    correct +=1
                else:
                    others_wrong += 1
            
            for i in question1.keys():
                if i in bans1:
                    for j in answer1[i]:
                        if j[0] not in bans1.values():
                            #this is the correct answer, so use that to query the database for the subtopic
                            if j[0] in topic:
                                continue
                            else:
                                topic.append(j[0])
                            
                else:
                    for j in answer1[i]:
                        if j[0] not in bans1.values():
                            #this is the correct answer, so use that to query the database for the subtopic
                            if j[0] in topic:
                                continue
                            else:
                                topic.append(j[0])
                
        
        
        for i in topic:
            it = dbloader.load_topic(subject, i)
            topic_final.append(it)
            
        # we need to better the recommendation for this side chale
            
        sub = Counter(topic_final).most_common(1)
        # gets the subtopic that got the most wrongs
        
        if sub[0][1] > 1: # if the wrongs are more than one, it sends it as a recommendation
            recommendation = sub[0][0][0][0].capitalize()
            
            if sub[0][1] < 4:
                recommendation_level = "Moderately Recommended"
            elif sub[0][1] >= 4:
                recommendation_level = "Highly Recommended"
            else:
                recommendation_level = ""
        else:
            recommendation = "None"
            recommendation_level = ""
        
        
        if sessions is 1 and current_user.is_authenticated:
            if subject == "social":
                current_user.social_points = current_user.social_points + (correct*2) - ( others_wrong*0.5)
            elif subject == "inter":
                current_user.inter_points= current_user.inter_points + (correct*2) - ( others_wrong*0.5)
            elif subject == "math":
                current_user.math_points = current_user.math_points + (correct*2) - ( others_wrong*0.5)
                
            progress = User_progress(user=current_user.id, last_subject = subject, last_score = correct, last_recommendation=recommendation)
            db.session.add(progress)
            db.session.commit()
            sessions = 0
        
        if current_user.is_authenticated:
            previous_crowns = current_user.user_achievement[-1].crowns # takes the number of crowns before recalculation
            temp_var = current_user.user_level + 1
                
            current_crowns = current_user.user_achievement[-1].crowns
            
            if previous_crowns > current_crowns:
                flash("You lost a crown!", 'success')
            elif previous_crowns < current_crowns:
                flash("You gained a crown!", 'success')
                
            if temp_var == current_user.user_level: # checks if the user has leveled up and the flashes a one time message on their page
                if flashed == 1:
                    flash('You have Leveled Up to Level 2!', 'success')
                    flash("You've gained the Silver Trophy!", 'success')
                elif flashed == 2:
                    flash('You have Leveled Up to Level 3!', 'success')
                    flash("You've gained the Gold Trophy!", 'success')
        
        if current_user.is_authenticated:
            level_checker = fxns.level_checker(current_user)
            subject_level = current_user.subject_level[-1]
        else:
            level_checker = 1
            subject_level = 1
        
        
        return render_template('resultspage.html', title='Your Score', correct=correct, subject = subject, q1 = questions_shuffle1, recommendation_level=recommendation_level,
        a1 = answer1, b1 = answered1, c1 = bans1, total=total, wrongs = others_wrong, recommendation = recommendation, subject_level=subject_level)

