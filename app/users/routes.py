from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import UpdateAccountForm
from app.models import User, User_streak, Subject_level, User_achievement, User_progress
from app.util import fxns, filters, token_fxn
from app.extensions import db
from app.decorators import check_confirmed
from datetime import datetime


users = Blueprint(
'users',
__name__,
static_folder = 'static',
template_folder = 'templates',
static_url_path = '/users'
)


@users.route('/confirm/<token>')
@login_required
def confirm_email(token): # email confirmation page
    
    try:
        email = token_fxn.confirm_token(token) # tests the user's token for validity 
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        
       
    user = User.query.filter_by(email=email).first_or_404() # if user has already confirmed
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else: # after confirmation, these are added to the db
        user.confirmed = True
        db.session.add(user)
        
        streak = User_streak(user=user.id, last_login= datetime.now()) # user's streak is initialized
        db.session.add(streak)
        
        subject_levels = Subject_level(user=user.id) 
        db.session.add(subject_levels)
        
        user_achievement = User_achievement(user=user.id)
        db.session.add(user_achievement)
        
        
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('users.haven')) # redirects to accounts page


# routes for unconfirmed accounts. They can login but they would always be redirected here
@users.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('haven')
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed_final.html')
    
    
# in case the person didn't get an email notification, and or the token got expired. They can be resent the confirmation mail 
# pretty simple to understand
@users.route('/resend')
@login_required
def resend_confirmation():
    token_resend = token_fxn.generate_confirmation_token(current_user.email)
    confirm_url = url_for('users.confirm_email', token=token_resend, _external=True)
    html = render_template('email_confirmation.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    fxns.send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('users.unconfirmed'))
 


@users.route("/haven", methods=['GET', 'POST'])
@login_required
@check_confirmed
def haven():
    user = current_user
    streak = user.user_streak[-1]
    form = UpdateAccountForm(email = current_user.email) # instance of the update account form, makes the email unchangeable 
    
    if request.method == "POST":
        try:
            default = request.form['default']
            if default == 'default':
                current_user.image_file = 'default.jpg'
                form.username.data = current_user.username
                flash('Your picture has been set to default', 'success')
                db.session.commit()
        except:
            if form.validate_on_submit():
                if form.picture.data:
                    picture_file = fxns.save_picture(form.picture.data) # function to save the picture
                    current_user.image_file = picture_file
                    
                user.username = form.username.data # fetches username from form in db
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('users.haven'))
            elif request.method == 'GET':
                form.username.data = current_user.username
                form.email.data = current_user.email
    else:
        form.username.data = current_user.username # when the page reloads sets the username, so the form isn't empty
                    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
                    
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    
    return render_template('haven_final.html', title = 'Haven', image_file=image_file, form=form, streak=streak)
    

@users.route("/logout")
def logout():
    logout_user() 
    return redirect(url_for('main.login'))




@users.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    user = current_user
    
    
    previous_crowns = user.user_achievement[-1].crowns # takes the number of crowns before recalculation
    
    temp_var = user.user_level + 1 # a temporal variable to hold the next level of the user
    
    level_checker = fxns.level_checker(user) # runs level checker and other inside things
    
    pro = user.user_progress # fetches user progress column
    
    subject_level = user.subject_level[-1] 
    flashed = level_checker[1] # takes the flag in the level_checker function
    current_crowns = user.user_achievement[-1].crowns
    current_trophy = user.user_achievement[-1].trophies
    
    if previous_crowns > current_crowns:
        flash("You lost a crown!", 'success')
    elif previous_crowns < current_crowns:
        flash("You gained a crown!", 'success')
    
    
    if temp_var == user.user_level: # checks if the user has leveled up and the flashes a one time message on their page
        if flashed == 1:
            flash('You have Leveled Up to Level 2!', 'success')
            flash("You've gained the Silver Trophy!", 'success')
        elif flashed == 2:
            flash('You have Leveled Up to Level 3!', 'success')
            flash("You've gained the Gold Trophy!", 'success')
        
    
    if 0 < len(pro): # checks to see if the user actually has any progress
        trial = 1
        progress = pro[-1]
        
    else:
        trial = 0
        progress = ""
    
    # these set of codes takes the first test and the mose recent test that they user has done, it is for the graph function
    last_english = User_progress.query.filter_by(author=user, last_subject='english').order_by(User_progress.date_taken.desc()).first()
    first_english = User_progress.query.filter_by(author=user, last_subject='english').order_by(User_progress.date_taken.asc()).first()
    
    last_social = User_progress.query.filter_by(author=user, last_subject='social').order_by(User_progress.date_taken.desc()).first()
    first_social = User_progress.query.filter_by(author=user, last_subject='social').order_by(User_progress.date_taken.asc()).first()
    
    last_math = User_progress.query.filter_by(author=user, last_subject='math').order_by(User_progress.date_taken.desc()).first()
    first_math = User_progress.query.filter_by(author=user, last_subject='math').order_by(User_progress.date_taken.asc()).first()
    
    last_inter =  User_progress.query.filter_by(author=user, last_subject='inter').order_by(User_progress.date_taken.desc()).first()
    first_inter =  User_progress.query.filter_by(author=user, last_subject='inter').order_by(User_progress.date_taken.asc()).first()
    
    if user.is_authenticated:
        streak = user.user_streak[-1]
    else:
        streak = "N/A"
        
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)    
    return render_template("Dashboard.html",image_file=image_file, progress=progress, trial=trial, subject_level=subject_level, streak=streak, last_english=last_english, last_math=last_math,
    last_social=last_social, last_inter=last_inter, current_crowns=current_crowns, first_english = first_english, first_math=first_math, first_inter=first_inter,
    first_social=first_social, current_trophy=current_trophy)



#@users.route("/account", methods=['GET', 'POST'])
#@login_required
#@check_confirmed
#def account(): #
#    user = current_user    
#    
#    
#    level_checker = fxns.level_checker(user) # runs level checker and other inside things
#    
#    pro = user.user_progress # fetches user progress column
#    
#    subject_level = user.subject_level[-1] 
#    flashed = level_checker[1] # takes the flag in the level_checker function
#        
#    if 0 < len(pro): # checks to see if the user actually has any progress
#        trial = 1
#        progress = pro[-1]
#        
#    else:
#        trial = 0
#        progress = ""
#     
#    
#    
#    form = UpdateAccountForm()  # instance of the update account form
#    if form.validate_on_submit():
#        if form.picture.data:
#            picture_file = fxns.save_picture(form.picture.data) # function to save the picture
#            current_user.image_file = picture_file
#        user.username = form.username.data # fetches username from form in db
#        user.email = form.email.data # fetches email data from form and replaces it in db
#        #remember that user = current_user, didn't notice? scroll up to the start of this funtion you'll see it tsw
#        db.session.commit()
#        flash('Your account has been updated!', 'success')
#        return redirect(url_for('users.account'))
#    elif request.method == 'GET':
#        form.username.data = current_user.username
#        form.email.data = current_user.email
#    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#    
#    return render_template('account.html', title='Account', image_file=image_file, form=form, progress=progress, trial=trial, subject_level=subject_level)



global selection
selection = "none"

global sorting
sorting = "none"

@users.route('/progress', methods=['GET', 'POST'], defaults={'page':1})
@users.route('/progress/page/<int:page>')
@login_required
@check_confirmed
def progress(page):
    user = current_user
    per_page = 20 # the number of results that'll appear per page on the progress page
    
    global selection 
    global sorting
    
    if request.method == 'POST': # checks if a form is posting data to the server, basically form submission
        try:
            sort = request.form['views'] # checks if a subject was selected to be viewed by
            selection = sort # then sets the global to that, the global is static so it isn't affected by refreshing
        except:
            sort = "all" 
            
        try:
            view = request.form['sort']
            sorting = view
        except:
            sorting = "none"
            
            
    else: # if the was no form submitted, this part runs
        if selection == "none":
            sort = "all"
            if sorting != "none":
                view = sorting
        else:
            sort = selection
            if sorting != "none":
                view = sorting
        
        
    # the trial variable decides which part of the code on the webpage shows
    # check progress.html
    if sort != 'all': # if there was a subject
        try:
            sorted = fxns.sort_by(sort, view, page, per_page) # it tries to sort it with the view and all
            trial = 2
        except:
        # using the object style to sort it
            sorted = User_progress.query.filter_by(author=user, last_subject=sort)\
            .order_by(User_progress.date_taken.desc())\
            .paginate(page=page, per_page=per_page)
            trial = 2
        
        if sorted.total == 0: # checks if the returned list is empty
            trial = 1
            
    
    else: # if there was no particular subject, well you get it
        try:
            sorted = fxns.sort_by(sort, view, page, per_page)
            trial = 2
        except:
        # read on sqlalchemy to get this
            sorted = User_progress.query.filter_by(author=user)\
            .order_by(User_progress.date_taken.desc())\
            .paginate(page=page, per_page=per_page)
            trial = 2
        
        if sorted.total == 0:
            trial = 0
          
        
    return render_template('allprogress.html', title='Progress Report', trial=trial, sorted=sorted, sort=sort, page=page)
        

    
 # the route to reset the password   
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm() #instance of the form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        fxns.send_reset_email(user)
        flash('An email has been sent to reset your password.', 'info')
        return redirect(url_for('main.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)
    


@users.route("/reset_password/<token>", methods=['GET', 'POST']) #we want to make sure it's the user with the specific token
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # the utf-8 makes it a string instead of bytes
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You can Login", 'success') # if all the forms filled are valid then flash the message and 'sucess' is a bootstrap class
        return redirect(url_for('main.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

