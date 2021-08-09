from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.util import fxns, filters, token_fxn
from app.extensions import db, bcrypt, mail

main = Blueprint(
'main',
__name__,
static_folder = 'static',
template_folder = 'templates',
static_url_path = '/main'
)


@main.route("/")
@main.route("/home")
def home():
    return redirect(url_for('main.login'))


@main.route("/index", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            try:
                login_user(user, remember=form.remember.data)
                #next_page = request.args.get('next') # the get method with () makes it optional, the square brackets will throw an error
                
                # so the below lines of code is mainly for the streak function
                login_time = datetime.now()
                last_login = user.user_streak[-1].last_login
         
                streak = fxns.streak_checker(login_time, last_login)
                user.user_streak[-1].current_streak = streak[0] 
                user.user_streak[-1].longest_streak = streak[1]
                user.user_streak[-1].last_login = login_time  
                user.user_streak[-1].streak_points += streak[2]
                db.session.commit()
                
                if streak[3] == 2:
                    flash("You Lost your streak! \n Use the site everyday to maintain it!", 'success')
                elif streak[3] == 1:
                    flash("Welcome Back", 'success')
                else:
                    flash("Congrats! You gained a point for maintaining you streak!", 'success')
                
                return redirect(url_for('users.haven')) 
            
            except:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('users.unconfirmed'))
            
        else:
            flash('Your email and password don\'t match! Please check and re-enter your details.', 'success')
    return render_template('Homepage.html', title = 'Home', form=form)



@main.route("/signup", methods = ['GET', 'POST'])
def signup():
    form =  RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # the utf-8 makes it a string instead of bytes
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, course=form.course_selection.data, confirmed = False) 
        # the above code instances the user code
        db.session.add(user)
        db.session.commit()
        
        #everytime you see the two above lines, we are committing stuff to the database
        
        token_confirm = token_fxn.generate_confirmation_token(user.email)  # function for confirming email
        
        confirm_url = url_for('users.confirm_email', token=token_confirm, _external=True)
        html = render_template('email_confirmation.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        fxns.send_email(user.email, subject, html)
        # sending the confirmation email
        
        
        login_user(user) # logs in user, remember our LoginManager? haq haq haq
        
        flash('A confirmation email has been sent via email.', 'success') # if all the forms filled are valid then flash the message and 'sucess' is a bootstrap class
        
        return redirect(url_for('users.unconfirmed'))
    return render_template ('signup.html', title = 'Join Us!', form=form)



@main.route("/about-dev")
def about_dev():
    return render_template('about_dev.html', title = 'About - Developers')


@main.route("/bugs", methods=['GET', 'POST'])
def bugs():
    if request.method == 'POST':
        report = request.form['report']
#        dbloader.load_bug_report(report) replace with the normal way of sqlalchemy
        flash("Thank You! Our team will get right on fixing the issues you've reported. :)", 'success')
    return render_template('bugs.html')


@main.route("/mobile-error", methods = ['GET'])
def mobile_response():
    return render_template('mobileresponse.html')
            
@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405

@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




