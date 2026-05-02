from flask import Flask, render_template,redirect,request,url_for,session,flash,jsonify,json,g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests

# for google authentication
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token

# for facebook athentication
# from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
# from flask_dance.consumer import oauth_authorized



# for phone number
import phonenumbers
from flask_bootstrap import Bootstrap

# for email password reset
from itsdangerous import URLSafeTimedSerializer

# for flask-pagination
from flask_paginate import Pagination, get_page_args

# for sending email
from flask_mail import Mail, Message

# for sending SMS
from twilio.rest import Client

# for create/download pdf
from flask import make_response
from xhtml2pdf import pisa
import io
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField, SubmitField, FileField, BooleanField, DateTimeLocalField, SelectMultipleField, widgets
from wtforms.validators import DataRequired,Email,ValidationError,EqualTo,Length

from wtforms import SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

# provides security during file upload
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# for storing env variables
import dotenv

from models import db, User, Question_Type, Question_Bank, Chapter, clClass, Semester, ExamStatus, Result, Schedule 
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
from flask import abort
# re module is used for regular expression matching
import re

import speech_recognition as sr

# shutil is used for file copy
import shutil

# for json question shuffling
import random

# using sqlite3 for testing
# ---------------------------------
import sqlite3
# ------------------------------

from qset_functions import *

# for accessing env variables (cotaining sensitive information)
dotenv.load_dotenv()

app = Flask(__name__)


# ----------------------------
# Get the absolute path to the directory where your app.py (or main) file is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Define the database path, joining the base directory with your desired filename
DATABASE_PATH = os.path.join(basedir, 'instance', 'onlinetest.db')
# Store the path in the Flask app's configuration
DATABASE = DATABASE_PATH

def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row  # This makes rows accessible like dictionaries
        return db
# ----------------------------------------------

# form classes
class RegisterForm(FlaskForm):
    username = StringField("Name",validators=[DataRequired(),Length(min=4,max=150)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=15)])
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo('password',message="Must match Password")])
    
    # custom validation

    def validate_username(self,field):
        hasusername = User.query.filter_by(username=field.data).first()
        if hasusername:
            raise ValidationError('Username already Taken')
        if not field.data[0].isalpha():
            raise ValidationError('Username slould start with an alphabate.')
        
    
    def validate_password(self, field):
            password = field.data
            # if len(password) < 8:
            #     raise ValidationError('Password must be at least 8 characters long.')
            if not any(char.isdigit() for char in password):
                raise ValidationError('Password must contain at least one digit.')
            if not any(char.isupper() for char in password):
                raise ValidationError('Password must contain at least one uppercase letter.')
            if not any(char.islower() for char in password):
                raise ValidationError('Password must contain at least one lowercase letter.')
            
            special_chars = r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]" # Define your allowed special characters
            if not re.search(special_chars, field.data):
                raise ValidationError('Password must contain at least one special character.')
           
    def validate_email(self,field):
        hasemail = User.query.filter_by(email=field.data).first()
        if hasemail:
            raise ValidationError('Email already Taken')

class LoginForm(FlaskForm):
    username = StringField("Name",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    
class UpdateForm(FlaskForm):  
    username = StringField("Username",validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired(), Email()])  

class Addquestion(FlaskForm):
    qclass = SelectField("Class",validators=[DataRequired()])
    qsem = SelectField("Semester",validators=[DataRequired()])
    qchapter = SelectField("Chapter",validators=[DataRequired()])
    qtype = SelectField("Question Type",validators=[DataRequired()])
    qhasimage = SelectField("wheather it contaings any Image",validators=[DataRequired()], choices=[("No","No"),("Yes","Yes")])
    qimagefile = FileField("Image File")
    qquestion = TextAreaField("Question",validators=[DataRequired(),Length(max=500)])
    qop1 = StringField("Option 1",validators=[DataRequired(),Length(max=200)])
    qop2 = StringField("Option 2",validators=[DataRequired(),Length(max=200)])
    qop3 = StringField("Option 3",validators=[DataRequired(),Length(max=200)])
    qop4 = StringField("Option 4",validators=[DataRequired(),Length(max=200)])
    qanswer = StringField("Correct Answer",validators=[DataRequired(),Length(max=200)])

class UpdateQuestionForm(FlaskForm):
    qclass = SelectField("Class",validators=[DataRequired()])
    qsem = SelectField("Semester",validators=[DataRequired()])
    qchapter = SelectField("Chapter",validators=[DataRequired()])
    qtype = SelectField("Question Type",validators=[DataRequired()])
    qhasimage = SelectField("wheather it contaings any Image",validators=[DataRequired()], choices=[("No","No"),("Yes","Yes")])
    qimagefile = FileField("Image File")
    # for file name display
    qfilename = StringField(" ")
    qquestion = StringField("Question",validators=[DataRequired(),Length(max=200)])
    qop1 = StringField("Option 1",validators=[DataRequired(),Length(max=200)])
    qop2 = StringField("Option 2",validators=[DataRequired(),Length(max=200)])
    qop3 = StringField("Option 3",validators=[DataRequired(),Length(max=200)])
    qop4 = StringField("Option 4",validators=[DataRequired(),Length(max=200)])
    qanswer = StringField("Correct Answer",validators=[DataRequired(),Length(max=200)])

class addChapter(FlaskForm):
    chclass = SelectField("Class",validators=[DataRequired()])
    chsem = SelectField("Semester",validators=[DataRequired()])
    chno = SelectField("Chapter Number",validators=[DataRequired()], choices=[(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),(6,"6"),(7,"7"),(8,"8"),(9,"9"),(10,"10"),(11,"11"),(12,"12"),(13,"13"),(14,"14"),(15,"15")])
    chdesc = StringField("Chapter Name",validators=[DataRequired(),Length(max=100)])

class addOrUpdateClass(FlaskForm):
    cldesc = StringField("Class Description",validators=[DataRequired(),Length(max=100)])

class addOrUpdateSemester(FlaskForm):
    smclass = SelectField("Class",validators=[DataRequired()])
    smdesc = StringField("Semester Description",validators=[DataRequired(),Length(max=100)])

class addOrUpdateQtype(FlaskForm):
    # qtypeno = SelectField("Question Type ID",validators=[DataRequired()], choices=[(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5"),(6,"6"),(7,"7"),(8,"8"),(9,"9"),(10,"10")])
    qtypedesc = StringField("Question Type Description",validators=[DataRequired(),Length(max=100)])

class MultiCheckboxField(SelectMultipleField):
    # """A multiple-select, except it displays a list of checkboxes."""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def pre_validate(self, form):
        pass

class setQuestion(FlaskForm):
    qclass = SelectField('Class', validators=[DataRequired()], choices=[])
    qsem = SelectField('Semester', validators=[DataRequired()], choices=[])
    qtype = MultiCheckboxField('Question Type', coerce=int, validators=[DataRequired()])
    qchapter = MultiCheckboxField('Chapter', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Generate')
    
    def __init__(self, *args, **kwargs):
        super(setQuestion, self).__init__(*args, **kwargs)
        self.qclass.choices = [(0, '-- Select Class --')]
        self.qsem.choices = [(0, '-- Select Semester --')]
        self.qtype.choices = []
        self.qchapter.choices = []
    
    def validate_qsem(self, field):
        if field.data and field.data != 0:
            class_id = self.qclass.data
            valid_ids = {s.sm_desc for s in Semester.query.filter_by(sm_class=class_id)}
            if field.data not in valid_ids:
                raise ValidationError('Invalid semester for selected class')
    
    def validate_qtype(self, field):
        if not field.data:
            raise ValidationError('Select at least one question type')
        
        # ALL = 0 সিলেক্ট করলে আর চেক লাগবে না
        if 0 in field.data:
            return
            
        valid_ids = {t.id for t in Question_Type.query.all()}
        if not set(field.data).issubset(valid_ids):
            raise ValidationError('Invalid question type selected')
    
    def validate_qchapter(self, field):
        if not field.data:
            raise ValidationError('Select at least one chapter')
        
        class_id = self.qclass.data
        sem_id = self.qsem.data
        
        # ALL = 0 সিলেক্ট করলে আর চেক লাগবে না
        if 0 in field.data:
            return
        
        if not class_id or not sem_id or class_id == 0 or sem_id == 0:
            raise ValidationError('Select class and semester first')
        
        valid_ids = {c.id for c in Chapter.query.filter_by(ch_class=class_id, ch_sem=sem_id)}
        if not set(field.data).issubset(valid_ids):
            raise ValidationError('Invalid chapter selected for this class/semester')
        """Custom validation to check if selected items belong to the qchapter."""
        if not field.data:
            raise ValidationError("Please select at least one item.")
        
            
class makeQuestionSet(FlaskForm):
    setno = SelectField("Number of Set", choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], validators=[DataRequired()])
    setalgo = SelectField("Select Algorithm", choices=[('1', 'random.shuffle()'), ('2', 'random.sample()'), ('3', 'Fisher-Yates shuffle'), ('4', 'random.randint(),pop()')], validators=[DataRequired()])
   
class ScheduleExam(FlaskForm): 
    # username = StringField("Name",validators=[DataRequired(),Length(min=4,max=150)])
    scheduleDateTime = DateTimeLocalField("Exam date and Time")
    examDuration = StringField("Exam Duration (in Minutes)",validators=[DataRequired(),Length(max=4)])
    examTimeDomaian = StringField("Max Time allowed for Exam (in Minutes)",validators=[DataRequired(),Length(max=200)])

class getEmail(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])

class forgotPasswordForm(FlaskForm):
    password = PasswordField("Password",validators=[DataRequired(),Length(min=4,max=15)])
    confirmpassword = PasswordField("Confirm Password", validators=[DataRequired(),EqualTo('password',message="Must match Password")])

class changePasswordForm(FlaskForm):
    oldpassword = PasswordField("Old Password",validators=[DataRequired(),Length(min=4,max=15)])
    newpassword = PasswordField("New Password",validators=[DataRequired(),Length(min=4,max=15)])
    confirmnewpassword = PasswordField("Confirm New Password", validators=[DataRequired(),EqualTo('password',message="Must match Password")])

class PhoneForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    # submit = SubmitField('Submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
        
# set up database

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlinetest.db'
app.config['UPLOAD_FOLDER'] = 'static/upload_files'
app.config['ANSWER_MATRIX'] = []
app.config['EXAM_INFO'] = []
app.config['SCHEDULE_INFO'] = ""
app.config['USERNAME'] = ""
app.config['TOTAL_MARKS'] = ""
app.config['OBTAINED_MARKS'] = "0"
app.config['VOICE_LANGUAGE'] = "BENG"
app.config['PROFILEPIC']="/static/images/profilePic2.png"

# for google authentication
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_OAUTH_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_OAUTH_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# Configure Facebook Blueprint
# facebook_blueprint = make_facebook_blueprint(
# client_id=os.getenv('FACEBOOK_OAUTH_CLIENT_ID'),
# client_secret=os.getenv('FACEBOOK_OAUTH_CLIENT_SECRET'),
# scope=["email", "public_profile"] # Request desired permissions
# )
# app.register_blueprint(facebook_blueprint, url_prefix="/login")

twitter = oauth.register(
        name='twitter',
        client_id='YOUR_TWITTER_CLIENT_ID',
        client_secret='YOUR_TWITTER_CLIENT_SECRET',
        # request_token_url=None, # Not needed for OAuth 2.0
        access_token_url='https://api.twitter.com/2/oauth2/token',
        authorize_url='https://twitter.com/i/oauth2/authorize',
        api_base_url='https://api.twitter.com/2/',
        client_kwargs={'scope': 'users.read tweets.read'}, # Adjust scopes as needed
        redirect_uri='http://localhost:5000/callback/twitter' # Must match your Twitter app's callback URL
    )

app.config['ALLOWED_EXTENSIONS'] = set(['png','jpg','jpeg','gif'])


# hooks(plug in) database to app
db.init_app(app)

# set up login_manager
login_manager = LoginManager()
# redirects unauthorized user to login page
login_manager.login_view ='login'
# hooks(plug in) login_manager to app
login_manager.init_app(app)


def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator


# remembers user across different pages (works automatically behind the scene)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ✅ Password reset token functions
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

# Returns the email if the token is valid, otherwise returns None
def verify_reset_token(token, expiration=3600):  # Valid for (3600s) i.e. 1 hour
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        return email
    except Exception as e:
        return None

def mailSetup():
# Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    mail = Mail(app)
    return mail




# ROUTE : /
@app.route('/')
def index():
    return redirect(url_for('login'))

# ROUTE : login
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
            
    if request.method == 'POST':

        repatcha_response = request.form.get('g-recaptcha-response')

        # captcha verification
        data = {
            'secret':os.getenv('RECAPTCHA_SECRET_KEY'),
            'response':repatcha_response
        }
        
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
        result = r.json()
        
        if not result.get('success'):
            flash("Captcha failed. Please try again.","danger")
            return redirect(url_for('login'))
            


        # check wheather user table is empty or not
        userexists = User.query.all()
        if not userexists:
            # create two sample records for guest user and admin user (FOR TESTING)
            user1 = User(username="pradipta", email="halderpradipta@gmail.com", password=generate_password_hash("123"), role="admin")
            user2 = User(username="ram", email="ram@gmail.com", password=generate_password_hash("111"), role="guest")
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            # create 7 dafault question types
            qt1 = Question_Type(qtype_desc ='Select the correct alternative MCQ (TYPE - I)')
            qt2 = Question_Type(qtype_desc ='Fill in the Blanks MCQ (TYPE - II)')
            qt3 = Question_Type(qtype_desc ='Match the columns')
            qt4 = Question_Type(qtype_desc ='State True / False')
            qt5 = Question_Type(qtype_desc ='Assertion Reasoning Type')
            qt6 = Question_Type(qtype_desc ='Diagram / Chart Based Type')
            qt7 = Question_Type(qtype_desc ='Drag and Drop Type')
            db.session.add_all([qt1, qt2, qt3, qt4, qt5, qt6, qt7])
            db.session.commit()
            
            flash("No User Exists. Please Register one User","danger")
            return redirect(url_for('register'))
            
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            if user.role == 'admin':
                flash("Logged in Successfully","success")
                return redirect(url_for('dashboard_admin'))
            else:
                app.config['USERNAME'] = user.username
                flash("Logged in Successfully","success")
                return redirect(url_for('dashboard_user'))
        else:
            flash("Invalid Credentials","danger")
            return redirect(url_for('login'))
    else:
         site_key = os.getenv('RECAPTCHA_SITE_KEY')
         return render_template('login.html',form=form,site_key=site_key)

# ROUTE : register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
       
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        # create users home directory
        basedir = os.path.abspath(os.path.dirname(__file__))
        directory_path = os.path.join(basedir, 'static', 'users') 
        
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        home_directory = os.path.join(directory_path,username)
        os.makedirs(home_directory)

        flash("Register Successfully. Please Login","success")
        return redirect(url_for('login'))
    else:
        return render_template('register.html',form=form)
    
# ROUTE : User Dashboard
@app.route('/dashboard_user')
@login_required
def dashboard_user():
    app.config['PROFILEPIC']="/static/images/profilePic2.png"
    profilePic = app.config['PROFILEPIC']
    return render_template('dashboard_user.html',user=current_user, profilePic=profilePic)

# ROUTE : Admin Dashboard (only used by admin)
@app.route('/dashboard_admin')
@login_required
@role_required('admin')
def dashboard_admin():
   app.config['PROFILEPIC']="/static/images/profilePic1.png"
   profilePic = app.config['PROFILEPIC']
   return render_template('dashboard_admin.html',user=current_user, profilePic=profilePic)

# ROUTE : User administration (only used by admin)
@app.route('/user_admin')
@login_required
@role_required('admin')
def user_admin():
    form = RegisterForm()
    if request.method == 'POST':
        pass
    else:
        allUser = User.query.all()
        # | (PIPE SIGN) IS USED AS FILTER IN JINJA2
        if Length(allUser)==0:
            flash("No User is found. Register your first User Now")
            return redirect('register.html',form=form)
        else:
            return render_template('user_admin.html',user=current_user,allUser=allUser)

# ROUTE : Update User (only used by admin)
@app.route('/update/<int:sno>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def update(sno):
    form = UpdateForm()
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        update_user = User.query.filter_by(id=sno).first()
        update_user.username = username
        update_user.email = email
        db.session.add(update_user)
        db.session.commit()
        return redirect("/user_admin")

    update_user = User.query.filter_by(id=sno).first()
    return render_template('update.html', update_user=update_user, form=form)

# ROUTE : Delete User (only used by admin)
@app.route('/delete/<int:sno>')
@login_required
@role_required('admin')
def delete(sno):
    # delete user from database
    delete_user = User.query.filter_by(id=sno).first()
    username = delete_user.username
    db.session.delete(delete_user)
    db.session.commit()
    flash("User Deleted Successfully from DB.","success")

    # deletes users home directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    directory_path = os.path.join(basedir, 'static', 'users',username) 
    
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            flash("User's Home Directory/contents deleted successfully.","success")
        except OSError as e:
            flash(f"Error deleting directory '{directory_path}': {e}","error")
    else:
        flash(f"Directory '{directory_path}' does not exist.","error")

    
    return redirect("/user_admin")


# ------------- ROUTE : CLASS ------------------------------

# ROUTE : Add Class (only used by admin)  
@app.route('/class/add_class', methods=["GET", "POST"])
@login_required 
@role_required('admin') 
def add_class():
    form = addOrUpdateClass()
    if request.method == 'POST' and form.validate_on_submit():
        cldesc = form.cldesc.data
        
        newclass = clClass(cl_desc=cldesc)
        db.session.add(newclass)
        db.session.commit()

        flash("Class Added Successfully","success")
        return redirect(url_for('add_class'))
    else:
        return render_template('add_class.html',form=form)
    
# ROUTE : Class Admin (only used by admin)  
@app.route('/class/class_admin', methods=["GET", "POST"])
@login_required
@role_required('admin')
def class_admin():
    form = addOrUpdateClass()
    if request.method == 'POST':
        pass
    else:
        allclass = clClass.query.order_by(clClass.cl_desc).all()
        # | (PIPE SIGN) IS USED AS FILTER IN JINJA2
        if allclass:
            return render_template('class_admin.html',user=current_user,allclass=allclass)
        else:                 
            flash("No class found. Add your first class Now","warning")
            return render_template('add_class.html',user=current_user,form=form)
        
# ROUTE : Update Class (only used by admin)
@app.route('/class/class_admin/update/<int:sno>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def update_class(sno):
    form = addOrUpdateClass()
    if request.method == "POST" and form.validate_on_submit():
        cldesc = request.form['cldesc']
                   
        updated_class = clClass.query.filter_by(id=sno).first()
        updated_class.cl_desc = cldesc
        db.session.add(updated_class)
        db.session.commit()
        flash("Class have been updated Successfully","success")
        return redirect("/class/class_admin")
        
    query_class = clClass.query.filter_by(id=sno).first()
    #  converts one record into a list and then jsonify it
    q = {
    'id': query_class.id,
    'cldesc': query_class.cl_desc,
    }
    updated_class=[]
    updated_class.append(q)
    return render_template('update_class.html', updated_class=updated_class, form=form)

# ROUTE : Delete Class (only used by admin)
@app.route('/class/class_admin/delete/<int:sno>')
@login_required
@role_required('admin')
def delete_class(sno):
    deleted_class = clClass.query.filter_by(id=sno).first()
    db.session.delete(deleted_class)
    db.session.commit()
    flash("Class have been deleted Successfully","success")
    return redirect("/class/class_admin")


# ------------- ROUTE : SEMESTER ------------------------------

# ROUTE : Add Semester (only used by admin)  
@app.route('/semester/add_semester', methods=["GET", "POST"])
@login_required 
@role_required('admin') 
def add_semester():
    form = addOrUpdateSemester()
    queryclass = clClass.query.order_by(clClass.cl_desc).all()

    # checks if class exists
    if queryclass:
            #  converts one record into a list and then jsonify it
            allclass=[]
            for item in queryclass:
                q = (item.cl_desc,item.cl_desc)
                allclass.append(q)
            form.smclass.choices=allclass

            # checks wheather is is post request or not
            if request.method == 'POST' and form.validate_on_submit():
                smclass = form.smclass.data
                smdesc = form.smdesc.data
                
                newsemester = Semester(sm_class=smclass,sm_desc=smdesc)
                db.session.add(newsemester)
                db.session.commit()

                flash("Semester Added Successfully","success")
                return redirect(url_for('add_semester'))
            
            else:
                return render_template('add_semester.html',form=form)
    
    #  if class does not exist, first create class
    else:
        flash("No class found. Add your first class Now","warning")
        form = addOrUpdateClass()
        return redirect(url_for('add_class',form=form))
            
# ROUTE : Semester Admin (only used by admin)  
@app.route('/semester/semester_admin', methods=["GET", "POST"])
@login_required
@role_required('admin')
def semester_admin():
    allsemester = Semester.query.order_by(Semester.sm_class,Semester.sm_desc).all()

    #  if semester record exists
    if allsemester:
        return render_template('semester_admin.html',user=current_user,allsemester=allsemester)
    else:
        flash("No semester is found. Add your first semester Now", "warning")
        return redirect(url_for('add_semester'))

# ROUTE : Update Semester (only used by admin)
@app.route('/semester/semester_admin/update/<int:sno>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def update_semester(sno):
    form = addOrUpdateSemester()
    queryclass = clClass.query.order_by(clClass.cl_desc).all()

    # populates class selectbox
    allclass=[]
    for item in queryclass:
        q = (item.cl_desc,item.cl_desc)
        allclass.append(q)
    form.smclass.choices=allclass

    if request.method == "POST" and form.validate_on_submit():
        smclass = request.form['smclass']
        smdesc = request.form['smdesc']
                   
        updated_semester = Semester.query.filter_by(id=sno).first()
        updated_semester.sm_class = smclass
        updated_semester.sm_desc = smdesc
        db.session.add(updated_semester)
        db.session.commit()
        flash("Semester has been updated Successfully","success")
        return redirect("/semester/semester_admin")
    
    else:
           
        query_semester = Semester.query.filter_by(id=sno).first()
        #  converts one record into a list and then jsonify it
        updated_semester=[]
        q = {
        'id': query_semester.id,
        'smclass' : query_semester.sm_class,
        'smdesc': query_semester.sm_desc
        }
        updated_semester.append(q)
        return render_template('update_semester.html', updated_semester=updated_semester, form=form)

# ROUTE : Delete Semester (only used by admin)
@app.route('/semester/semester_admin/delete/<int:sno>')
@login_required
@role_required('admin')
def delete_semester(sno):
    deleted_semester = Semester.query.filter_by(id=sno).first()
    db.session.delete(deleted_semester)
    db.session.commit()
    flash("Semester has been deleted Successfully","success")
    return redirect("/semester/semester_admin")


# ------------- ROUTE : CHAPTER ------------------------------

# ROUTE : Add Chapter (only used by admin)  
@app.route('/chapter/add_chapter', methods=["GET", "POST"])
@login_required 
@role_required('admin') 
def add_chapter():
    form = addChapter()
    queryclass = clClass.query.order_by(clClass.cl_desc).all()
    querysemester = Semester.query.order_by(Semester.sm_class).all()

    # checks if semester exists
    if querysemester:
        
        # populates class selectbox
        allclass=[]
        for item in queryclass:
            q = (item.cl_desc,item.cl_desc)
            allclass.append(q)
        form.chclass.choices=allclass

        # populates semester selectbox
        allsemester=[]
        for item in querysemester:
            q = (item.sm_desc,item.sm_desc)
            allsemester.append(q)
        form.chsem.choices=allsemester

        # checks wheather is is post request or not
        if request.method == 'POST' and form.validate_on_submit():
            cclass = form.chclass.data
            csem = form.chsem.data
            cno = form.chno.data
            cdesc = form.chdesc.data
            newchapter = Chapter(ch_class=cclass, ch_sem=csem, ch_no=cno, ch_desc=cdesc)
            db.session.add(newchapter)
            db.session.commit()

            flash("Chapter has been added Successfully","success")
            return redirect(url_for('add_chapter'))
        else:
            return render_template('add_chapter.html',form=form)


    #  if semester does not exist, first create semester
    else:
        flash("No semester found. Add your first semester Now","warning")
        form = addOrUpdateSemester()
        return redirect(url_for('add_semester',form=form))

    
# ROUTE : Chapter Admin (only used by admin)  
@app.route('/chapter/chapter_admin', methods=["GET", "POST"])
@login_required
@role_required('admin')
def chapter_admin():
    form = addChapter()
    allchapter = Chapter.query.order_by(Chapter.ch_class, Chapter.ch_sem,Chapter.ch_no).all()
    if allchapter:
        return render_template('chapter_admin.html',user=current_user,allchapter=allchapter)     
    else:
        flash("No chapter found. Add your first chapter Now","warning")
        return redirect(url_for('add_chapter',form=form))
        
# ROUTE : Update Chapter (only used by admin)
@app.route('/chapter/chapter_admin/update/<int:sno>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def update_chapter(sno):
    form = addChapter()

    queryclass = clClass.query.order_by(clClass.cl_desc).all()
    querysemester = Semester.query.order_by(Semester.sm_class).all()

    # populates class selectbox
    allclass=[]
    for item in queryclass:
        q = (item.cl_desc,item.cl_desc)
        allclass.append(q)
    form.chclass.choices=allclass

    # populates semester selectbox
    allsemester=[]
    for item in querysemester:
        q = (item.sm_desc,item.sm_desc)
        allsemester.append(q)
    form.chsem.choices=allsemester


    if request.method == "POST" and form.validate_on_submit():
        uchclass = request.form['chclass']
        uchsem = request.form['chsem']
        uchno = request.form['chno']
        uchdesc = request.form['chdesc']
                   
        updated_chapter = Chapter.query.filter_by(id=sno).first()
        updated_chapter.ch_class = uchclass
        updated_chapter.ch_sem = uchsem
        updated_chapter.ch_no = uchno
        updated_chapter.ch_desc = uchdesc
        db.session.add(updated_chapter)
        db.session.commit()
        flash("Chapter have been updated Successfully","success")
        return redirect("/chapter/chapter_admin")
        
    query_chapter = Chapter.query.filter_by(id=sno).first()
    #  converts one record into a list and then jsonify it
    q = {
    'id': query_chapter.id,
    'chclass' : query_chapter.ch_class,
    'chsem' : query_chapter.ch_sem,
    'chno': query_chapter.ch_no, 
    'chdesc': query_chapter.ch_desc,
    }
    updated_chapter=[]
    updated_chapter.append(q)
    return render_template('update_chapter.html', updated_chapter=updated_chapter, form=form)

# ROUTE : Delete Chapter (only used by admin)
@app.route('/chapter/chapter_admin/delete/<int:sno>')
@login_required
@role_required('admin')
def delete_chapter(sno):
    deleted_chapter = Chapter.query.filter_by(id=sno).first()
    db.session.delete(deleted_chapter)
    db.session.commit()
    flash("Chapter have been deleted Successfully","success")
    return redirect("/chapter/chapter_admin")

# ------------- ROUTE : QTYPE ------------------------------

# ROUTE : Add question type (only used by admin)   
@app.route('/qtype/add_qtype', methods=["GET", "POST"])
@login_required
@role_required('admin')
def add_qtype():
    form = addOrUpdateQtype()
     # checks wheather is is post request or not
    if request.method == 'POST' and form.validate_on_submit():
        # qtno = form.qtypeno.data
        qtypedesc = form.qtypedesc.data
        
        newqtype = Question_Type(qtype_desc=qtypedesc)
        db.session.add(newqtype)
        db.session.commit()

        flash("Qtype has been added Successfully","success")
        return redirect(url_for('add_qtype'))
    else:
        return render_template('add_qtype.html',form=form)
    
# ROUTE : Question type admin (only used by admin)   
@app.route('/qtype/qtype_admin', methods=["GET", "POST"])
@login_required
@role_required('admin')
def qtype_admin():
    form = addOrUpdateQtype
    allqtype =  Question_Type.query.order_by( Question_Type.id).all()
    if allqtype:
        return render_template('qtype_admin.html',user=current_user,allqtype=allqtype)     
    else:
        flash("No Question Type found. Add your first Question Type Now","warning")
        return redirect(url_for('add_qtype',form=form))


# ROUTE : Update Question Type (only used by admin)
@app.route('/qtype/qtype_admin/update/<int:sno>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def update_qtype(sno):
    form = addOrUpdateQtype()
    if request.method == "POST" and form.validate_on_submit():
        uchdesc = request.form['qtypedesc']
                   
        updated_qtype = Question_Type.query.filter_by(id=sno).first()
        updated_qtype.qtype_desc = uchdesc
        db.session.add(updated_qtype)
        db.session.commit()
        flash("Question Type has been updated Successfully","success")
        return redirect("/qtype/qtype_admin")
        
    query_qtype = Question_Type.query.filter_by(id=sno).first()
    #  converts one record into a list and then jsonify it
    q = {
    'id': query_qtype.id,
    'qtypedesc': query_qtype.qtype_desc,
    }
    updated_qtype=[]
    updated_qtype.append(q)
    return render_template('update_qtype.html', updated_qtype=updated_qtype, form=form)


# ROUTE : Delete Question type (only used by admin)
@app.route('/qtype/qtype_admin/delete/<int:sno>')
@login_required
@role_required('admin')
def delete_qtype(sno):
    deleted_qtype =  Question_Type.query.filter_by(id=sno).first()
    db.session.delete(deleted_qtype)
    db.session.commit()
    flash("Question has been deleted Successfully","success")
    return redirect("/qtype/qtype_admin")






# ------------- ROUTE : QUESTION ------------------------------

# ROUTE : Add question to Question Bank (only used by admin)   
@app.route('/add_question', methods=["GET", "POST"])
@login_required
@role_required('admin')
def add_question():
     form = Addquestion()
     querychapter = Chapter.query.order_by(Chapter.ch_no).all()
     queryclass = clClass.query.order_by(clClass.cl_desc).all()
     querysemester = Semester.query.order_by(Semester.sm_desc).all()
     queryqtype = Question_Type.query.order_by(Question_Type.id).all()

     # checks if Chapter exists
     if querychapter:

         # populates class selectbox
        allclass=[]
        for item in queryclass:
            q = (item.cl_desc,item.cl_desc)
            allclass.append(q)
        form.qclass.choices=allclass

        # populates semester selectbox
        allsemester=[]
        for item in querysemester:
            q = (item.sm_desc,item.sm_desc)
            allsemester.append(q)
        form.qsem.choices=allsemester

        # populates chapter selectbox
        allchapter=[]
        for item in querychapter:
            q = (item.ch_no,item.ch_desc)
            allchapter.append(q)
        form.qchapter.choices=allchapter

        # populates qtype selectbox
        allqtype=[]
        for item in queryqtype:
            q = (item.id,item.qtype_desc)
            allqtype.append(q)
        form.qtype.choices=allqtype

        if request.method == 'POST' and form.validate_on_submit():
            qclass = form.qclass.data
            qsem = form.qsem.data
            qchapter = form.qchapter.data
            qtype = form.qtype.data
            qhasimage = form.qhasimage.data

            uploaded_file = form.qimagefile.data
            filename = ""
            # if uploaded_file and allowed_file(uploaded_file):
            if uploaded_file:
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            
            qquestion = form.qquestion.data
            qop1 = form.qop1.data
            qop2 = form.qop2.data
            qop3 = form.qop3.data
            qop4 = form.qop4.data
            qanswer = form.qanswer.data
   
            newquestion = Question_Bank(studyclass=qclass, sem=qsem, chapter=qchapter, Question_Type_id=qtype, hasimage=qhasimage, imagelocation=filename, question=qquestion, op1=qop1, op2=qop2, op3=qop3, op4=qop4, answer=qanswer)
            db.session.add(newquestion)
            db.session.commit()

            flash("Question Added Successfully","success")
            return redirect(url_for('add_question'))
        else:
            return render_template('add_question.html',form=form)

     else:
        flash("No chapter found. Add your first chapter Now","warning")
        form = addChapter()
        return redirect(url_for('add_chapter',form=form))
    
     
# ROUTE : Question administration (only used by admin)
@app.route('/question_admin')
@login_required
@role_required('admin')
def question_admin():
    form = Addquestion()

    if request.method == 'POST':
        pass
    else:
        questionBank = Question_Bank.query.all()
        
        # if questionbank is empty
        if not questionBank:
            flash("No Question is found. Add your first question Now","warning")
            return redirect(url_for('add_question',form=form))
        else:
            # page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

            # # Get data for the current page
            # paginated_users = questionBank[offset: offset + per_page]

            # # Initialize Pagination object
            # pagination = Pagination(page=page, per_page=per_page, total=len(questionBank),
            #                         css_framework='bootstrap5') # Or 'bootstrap5'
    
            # return render_template('question_admin.html',user=current_user, 
            #                     questionBank=paginated_users, 
            #                     page=page, 
            #                     per_page=per_page, 
            #                     pagination=pagination)

            return render_template('question_admin.html',user=current_user,questionBank=questionBank)

# ROUTE : Update Question (only used by admin)
@app.route('/question/update/<int:sno>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def update_question(sno):
    form = UpdateQuestionForm()
    querychapter = Chapter.query.order_by(Chapter.ch_no).all()
    queryclass = clClass.query.order_by(clClass.cl_desc).all()
    querysemester = Semester.query.order_by(Semester.sm_class).all()
    queryqtype = Question_Type.query.order_by(Question_Type.id).all()

    # checks if any chapter exists
    if querychapter:

        # populates class selectbox
        allclass=[]
        for item in queryclass:
            q = (item.cl_desc,item.cl_desc)
            allclass.append(q)
        form.qclass.choices=allclass

        # populates semester selectbox
        allsemester=[]
        for item in querysemester:
            q = (item.sm_desc,item.sm_desc)
            allsemester.append(q)
        form.qsem.choices=allsemester

        # populates chapter selectbox
        allchapter=[]
        for item in querychapter:
            q = (item.ch_no,item.ch_desc)
            allchapter.append(q)
        form.qchapter.choices=allchapter

        # populates qtype selectbox
        allqtype=[]
        for item in queryqtype:
            q = (item.id,item.qtype_desc)
            allqtype.append(q)
        form.qtype.choices=allqtype

    if request.method == "POST" and form.validate_on_submit():
        ustudyclass = request.form['qclass']
        usem = request.form['qsem']
        uhasimage = request.form['qhasimage']

        uploaded_file = form.qimagefile.data
        filename1 = ""
        # if uploaded_file and allowed_file(uploaded_file):
        if uploaded_file:
            filename1 = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename1))
            
        uimagelocation = filename1
        uquestion = request.form['qquestion']
        uop1 = request.form['qop1']
        uop2 = request.form['qop2']
        uop3 = request.form['qop3']
        uop4 = request.form['qop4']
        uanswer = request.form['qanswer']
            
        updated_question = Question_Bank.query.filter_by(id=sno).first()
        updated_question.studyclass = ustudyclass
        updated_question.sem = usem
        updated_question.hasimage = uhasimage
        updated_question.imagelocation = uimagelocation
        updated_question.question = uquestion
        updated_question.op1 = uop1
        updated_question.op2 = uop2
        updated_question.op3 = uop3
        updated_question.op4 = uop4
        updated_question.answer = uanswer
        db.session.add(updated_question)
        db.session.commit()
        flash("Question have been updated Successfully","success")
        return redirect("/question_admin")
        
    query_question = Question_Bank.query.filter_by(id=sno).first()
    #  converts one record into a list and then jsonify it
    q = {
    'id': query_question.id,
    'studyclass' : query_question.studyclass,
    'sem' : query_question.sem,
    'chapter' : query_question.chapter,
    'Question_Type_id' : query_question.Question_Type_id,
    'hasimage': query_question.hasimage, 
    'imagelocation': query_question.imagelocation,
    'question' : query_question.question, 
    'op1' : query_question.op1,
    'op2' : query_question.op2,
    'op3' : query_question.op3,
    'op4' : query_question.op4,
    'answer' : query_question.answer
    }
    updated_question=[]
    updated_question.append(q)
    return render_template('updatequestion.html', updated_question=updated_question, form=form)

# ROUTE : Delete Question (only used by admin)
@app.route('/question/delete/<int:sno>')
@login_required
@role_required('admin')
def delete_question(sno):
    deleted_question = Question_Bank.query.filter_by(id=sno).first()
    db.session.delete(deleted_question)
    db.session.commit()
    flash("Question have been deleted Successfully","success")
    return redirect("/question_admin")

# ROUTE : Before Start Exam (used by guest)  
@app.route('/exam/before_start_exam', methods=["GET", "POST"])
@login_required  
def before_start_exam():
    
    # read the content of examInfo JSON file
        basedir = os.path.abspath(os.path.dirname(__file__))
        exam_Infofile_path = os.path.join(basedir, 'static', 'Exam', 'ExamInfo.json')
                        
        # read examinfo JSON
        try:
            with open(exam_Infofile_path, 'r') as f:
                # read the content of examInfo JSON file
                result = json.load(f)
                app.config['EXAM_INFO'] = result
                scheduleinfo = result[0]['Schedule']
                
                # check if exam is already submitted
                examstatus = ExamStatus.query.filter_by(user_id=current_user.id,schedule=scheduleinfo,exam_status="Submitted").first()
                if(examstatus):
                    status = [{"stat": "Yes"}]
                else:
                    status = [{"stat": "No"}]
                
                return render_template('before_start_exam.html',result=result,examstat=status)
                                                
        except FileNotFoundError:
            return "Error: JSON File not found"
        except json.JSONDecodeError:
            return "Error: Error decoding JSON" 
        

# ROUTE : Start Exam (used by guest)  
@app.route('/exam/start_exam', methods=["GET", "POST"])
@login_required  
def start_exam():
    # questions = Question_Bank.query.all()
    # result = []
    # #  converts each record into array of objects and then add it to dictionary object
    # for row in questions:
    #     item = {
    #         'id': row.id,
    #         'studyclass' : row.studyclass,
    #         'sem' : row.sem,
    #         'chapter' : row.chapter,
    #         'questiontype' : row.parent_Question_Type.qtype_desc,
    #         'hasimage': row.hasimage, 
    #         'imagelocation': row.imagelocation,
    #         'question' : row.question, 
    #         'choices' : [row.op1,row.op2,row.op3,row.op4],
    #         'answer' : row.answer
    #         }
    #     result.append(item)


    # check for disaster question set
    
    # read the content of examInfo JSON file
    basedir = os.path.abspath(os.path.dirname(__file__))
    exam_Infofile_path = os.path.join(basedir, 'static', 'Exam', 'ExamInfo.json')
    directory_path = os.path.join(basedir, 'static', 'Exam')  
    scheduleinfo = ""
    setName = ""
    JSON_FILE =""
    userid = current_user.id

    try:
        with open(exam_Infofile_path, 'r') as f:
            app.config['EXAM_INFO'] = json.load(f)
            examinfo = app.config['EXAM_INFO']
            scheduleinfo = examinfo[0]['Schedule']
            # also saves examinfo in the global var
            app.config['SCHEDULE_INFO'] = scheduleinfo
            
    except FileNotFoundError:
        return jsonify({"error": "JSON file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500   
    
    # check if examstatus exists for the user and exam schedule
    examstatus = ExamStatus.query.filter_by(user_id=userid,schedule=scheduleinfo).first()
    
    if(examstatus):
         # retrieve saved set name from table
        setName = examstatus.set_name 
        filename = setName + ".json"
        JSON_FILE = os.path.join(directory_path,filename)
                
        try:
            with open(JSON_FILE, 'r') as f:
                result = json.load(f)
                return render_template('start_exam.html',result=result,setName=setName,examinfo=examinfo)
        
        except FileNotFoundError:
            return jsonify({"error": "JSON file not found"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Error decoding JSON"}), 500 

    
    else:
        # choose random question set
        JSON_FILE = chooseRandomSet(directory_path,"S*.json")
        setName = getSetName(JSON_FILE)

        # create one new record in the examstatus table
        newstatus = ExamStatus(user_id=userid, schedule=scheduleinfo, set_name=setName, exam_status="Started")
        db.session.add(newstatus)
        db.session.commit()

        try:
            with open(JSON_FILE, 'r') as f:
                result = json.load(f)
                return render_template('start_exam.html',result=result,setName=setName,examinfo=examinfo)
        
        except FileNotFoundError:
            return jsonify({"error": "JSON file not found"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Error decoding JSON"}), 500 
    

@app.route('/exam/set_question', methods=["GET", "POST"])
@login_required
@role_required('admin')
def set_question():
    form = setQuestion()

    # queryclass = clClass.query.order_by(clClass.cl_class).all()
    querychapter = Chapter.query.order_by(Chapter.ch_no).all()
    
    # checks if Chapter exists
    if querychapter:
            
        # if request.method == 'POST':
        #     qclass = form.qclass.data
        #     qsem = form.qsem.data
            
        #     # IMPORTANT: Manually set choices for class
        #     all_classes = clClass.query.all() 
        #     form.qclass.choices = [(c.cl_desc, c.cl_desc) for c in all_classes]

        #     # IMPORTANT: Manually set choices for semester
        #     all_sems = Semester.query.filter_by(sm_class=form.qclass.data).all() 
        #     form.qsem.choices = [(s.sm_desc, s.sm_desc) for s in all_sems]

        #     # IMPORTANT: Manually set choices for question type
        #     qtypes = Question_Type.query.order_by(Question_Type.id).all()
        #     form.qtype.choices.clear()
        #     form.qtype.choices = [0,0]+[(i.id, i.qtype_desc) for i in qtypes]

        #     # IMPORTANT: Manually set choices based on the submitted class and sem
        #     # so WTForms can process the 'chapter' data.
        #     if form.qclass.data and form.qsem.data:
        #         form.qchapter.choices.clear()
        #         chapters = Chapter.query.filter_by(ch_class=form.qclass.data,ch_sem=form.qsem.data).all()
        #         form.qchapter.choices = [0,0]+[(i.id, i.ch_desc) for i in chapters]
        #     # else:
        #     #     form.qchapter.choices = [] # Ensure it's an empty list, not None

           
        #     # multiselect checkbox list validation (qtype and chapter)
        #     if form.validate_on_submit():
        #         # Process form.items.data (this will be a list of IDs)
        #         # 'qchapter' refers to the 'name' attribute of your HTML/JS checkboxes
        #         selected_chapter = request.form.getlist('qchapter')
        #         # as list can't be sent, converting it into a comma separated string
        #         serialized_chapter = ",".join(selected_chapter)

        #         # 'qtype' refers to the 'name' attribute of your HTML/JS checkboxes
        #         selected_qtype = request.form.getlist('qtype')
        #         # as list can't be sent, converting it into a comma separated string
        #         serialized_qtype = ",".join(selected_qtype)
        #         return redirect(url_for('get_question_list',qclass=qclass,qsem=qsem,qchapter=serialized_chapter,qtype=serialized_qtype))

        if request.method == 'POST':
            # POST এ choices সেট করা মাস্ট
            class_id = form.qclass.data
            sem_id = form.qsem.data
       
            # 1. qclass, qsem এর choices
            if class_id and class_id != 0:
                form.qclass.choices = [(0, '-- Select Class --')] + [(c.cl_desc, c.cl_desc) for c in clClass.query.all()]
                form.qsem.choices = [(0, '-- Select Semester --')] + [(s.sm_desc, s.sm_desc) for s in Semester.query.filter_by(sm_class=class_id)]
                
            # 2. qtype এর choices + ALL
                form.qtype.choices = [(0, 'ALL Types')] + [(t.id, t.qtype_desc) for t in Question_Type.query.all()]
        
            # 3. qchapter এর choices + ALL
            if  class_id and sem_id and class_id != 0 and sem_id != 0:
                chapters = [(c.id, c.ch_desc) for c in Chapter.query.filter_by(ch_class=class_id, ch_sem=sem_id)]
                form.qchapter.choices = [(0, 'ALL Chapters')] + chapters
                print(form.qchapter.choices)
    
            if form.validate_on_submit():
                class_id = form.qclass.data
                sem_id = form.qsem.data
                qtypes = form.qtype.data
                qchapters = form.qchapter.data

                # ALL সিলেক্ট করলে সব আইডি রিপ্লেস
                if 0 in qtypes:
                    qtypes = [t.id for t in Question_Type.query.all()]

                if 0 in qchapters:
                    qchapters = [c.id for c in Chapter.query.filter_by(ch_class=class_id, ch_sem=sem_id)]

                # return f"OK: Class={class_id}, Sem={sem_id}, Types={qtypes}, Chapters={qchapters}"
                # Process form.items.data (this will be a list of IDs)
                # 'qchapter' refers to the 'name' attribute of your HTML/JS checkboxes
                selected_chapter = request.form.getlist('qchapter')
                # as list can't be sent, converting it into a comma separated string
                serialized_chapter = ",".join(selected_chapter)

                # 'qtype' refers to the 'name' attribute of your HTML/JS checkboxes
                selected_qtype = request.form.getlist('qtype')
                # as list can't be sent, converting it into a comma separated string
                serialized_qtype = ",".join(selected_qtype)
                return redirect(url_for('get_question_list',qclass=class_id,qsem=sem_id,qchapter=serialized_chapter,qtype=serialized_qtype))
    
            return render_template('set_question.html',form=form)
        
        else:
            return render_template('set_question.html',form=form)
        
    else:
        flash("No chapter found. Add your first chapter Now","warning")
        form = addChapter()
        return redirect(url_for('add_chapter',form=form))


@app.route('/exam/get_question_list/<qclass>/<qsem>/<qchapter>/<qtype>', methods=["GET", "POST"])
@login_required
@role_required('admin')
def get_question_list(qclass,qsem,qchapter,qtype):
        db = get_db()

        # convert comma separated chapter back into list
        qchapter_list = qchapter.split(',') if qchapter else []
        print(f"Chapter: {qchapter_list}")

        # convert comma separated qtype back into list
        qtype_list = qtype.split(',') if qtype else []
        print(f"Qtype: {qtype_list}")

        if (('0' in qchapter_list) and ('0' in qtype_list)):
            cursor = db.execute('SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ?', [qclass,qsem])
        
        elif (('0' in qchapter_list) and ('0' not in qtype_list)):
            # 1. Generate placeholders: "?, ?, ?" for qtype
            placeholders = ', '.join(['?'] * len(qtype_list))
            # 2. Build the query string
            query = f"SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ? AND Question_Type_id IN ({placeholders})"
            print(query)
            # 3. Flatten all parameters into a single list
            params = [qclass] + [qsem] + qtype_list
            #4. Execute Results
            cursor=db.execute(query, params)

        elif (('0' not in qchapter_list) and ('0' in qtype_list)):
            # 1. Generate placeholders: "?, ?, ?" for qchapter
            placeholders = ', '.join(['?'] * len(qchapter_list))
            # 2. Build the query string
            query = f"SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ? AND chapter IN ({placeholders})"
            print(query)
            # 3. Flatten all parameters into a single list
            params = [qclass] + [qsem] + qchapter_list
            #4. Execute Results
            cursor=db.execute(query, params)
        
        else:
            # 1. Generate placeholders: "?, ?, ?" for qchapter
            placeholders1 = ', '.join(['?'] * len(qchapter_list))
            # Generate placeholders: "?, ?, ?" for qtype
            placeholders2 = ', '.join(['?'] * len(qtype_list))

            # 2. Build the query string
            query = f"SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ? AND chapter IN ({placeholders1}) AND Question_Type_id IN ({placeholders2})"
            print(query)
            # 3. Flatten all parameters into a single list
            params = [qclass] + [qsem] + qchapter_list + qtype_list

            #4. Execute Results
            cursor=db.execute(query, params)

        # fetch results
        allquestion = cursor.fetchall()
            
        # if qchapter=="0" and qtype=="0":
        #     cursor = db.execute('SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ?', [qclass,qsem])
        # elif qchapter=="0" and qtype!="0":
        #     cursor = db.execute('SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ? AND Question_Type_id = ?', [qclass,qsem,qtype])
        # elif qchapter!="0" and qtype=="0":
        #     cursor = db.execute('SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ? AND chapter = ?', [qclass,qsem,qchapter])
        # else:
        #     cursor = db.execute('SELECT * FROM Question_Bank WHERE studyclass = ? AND sem = ? AND chapter = ? AND Question_Type_id = ?', [qclass,qsem,qchapter,qtype])

        # gathering exam info (class, sem, chapter, qtype)
        examClass = qclass
        examSem = qsem
        
        # if qchapter=="0":
        #      examChapter = "ALL"
        # else:
        #     cursor = db.execute('SELECT * FROM Chapter WHERE id = ?', [qchapter])
        #     examChapterRecord = cursor.fetchone()
        #     examChapter = examChapterRecord['ch_desc']
        
        # if qtype=="0":
        #      examQtype = "ALL"
        # else:
        #     cursor = db.execute('SELECT * FROM Question_Type WHERE id = ?', [qtype])
        #     examQtypeRecord = cursor.fetchone()
        #     examQtype = examQtypeRecord['qtype_desc']

        if '0' in qchapter_list:
             examChapter = "ALL"
        else:
            # 1. Generate placeholders: "?, ?, ?" for qchapter
            placeholders = ', '.join(['?'] * len(qchapter_list))
            # 2. Build the query string
            query = f"SELECT * FROM Chapter WHERE id IN ({placeholders})"
            print(query)
            # 3. Flatten all parameters into a single list
            params = qchapter_list
            # 4. Execute Results
            cursor=db.execute(query, params)
            # 5. Fetch all Chapters
            examChapterRecord = cursor.fetchall()
            # 6. Extracts 'column_name' from each row and joins them with a comma
            examChapter = ", ".join([str(row['ch_desc']) for row in examChapterRecord])
            
        
        if '0' in qtype_list:
             examQtype = "ALL"
        else:
            # 1. Generate placeholders: "?, ?, ?" for qtype
            placeholders = ', '.join(['?'] * len(qtype_list))
            # 2. Build the query string
            query = f"SELECT * FROM Question_Type WHERE id IN ({placeholders})"
            print(query)
            # 3. Flatten all parameters into a single list
            params = qtype_list
            # 4. Execute Results
            cursor=db.execute(query, params)
            # 5. Fetch all Question Type
            examQtypeRecord = cursor.fetchall()
            # 6. Extracts 'column_name' from each row and joins them with a comma
            examQtype = ", ".join([str(row['qtype_desc']) for row in examQtypeRecord])

        return render_template('get_question_list.html',allquestion=allquestion,examClass=examClass,examSem=examSem,examChapter=examChapter,examQtype=examQtype)

@app.route('/exam/schedule_exam', methods=["GET", "POST"])
@login_required
@role_required('admin')
def schedule_exam():
    update_schedule_table=[]
    form = ScheduleExam()
    if request.method == 'POST':
        scheduleInfo = form.scheduleDateTime.data
        examduration = form.examDuration.data
        examtimedomain = form.examTimeDomaian.data
        
        # read the content of examInfo JSON file
        basedir = os.path.abspath(os.path.dirname(__file__))
        datafile_path = os.path.join(basedir, 'static', 'Exam', 'data.json')
        exam_Infofile_path = os.path.join(basedir, 'static', 'Exam', 'ExamInfo.json')
        directory_path = os.path.join(basedir, 'static', 'Exam')  
        read_content=[]
        
        # read examinfo JSON & append scheduleinfo to it
        try:
            with open(exam_Infofile_path, 'r') as f:
                 # read the content of examInfo JSON file
                read_content = json.load(f)
                # append the schedule content to the dictionary
                item = read_content[0]
                item["Schedule"] = scheduleInfo.strftime("%Y-%m-%d %H:%M:%S")
                item["ExamDuration"] = examduration
                item["ExamTimeDomain"] = examtimedomain
                update_schedule_table=item

        except FileNotFoundError:
            return jsonify({"error": "JSON file not found"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Error decoding JSON"}), 500  
          
         # Write modified examinfo JSON
        try:
            with open(exam_Infofile_path,'w') as f:
                json.dump(read_content, f, indent=4) # indent for readability
                flash("Schedule Info created successfully","success")
                
                # add new schedule info record to table
                sclass = update_schedule_table["Class"]
                semester = update_schedule_table["Sem"]
                chap = update_schedule_table["Chapter"]
                qttype = update_schedule_table["QuestionType"]
                sch = update_schedule_table["Schedule"]
                exduration = update_schedule_table["ExamDuration"]
                extimedomain = update_schedule_table["ExamTimeDomain"]
                createdon = datetime.now()

                sinfo=Schedule(studyclass=sclass,sem=semester,chapter=chap,qtype=qttype,sch=sch,examduration=exduration,examtimedomain=extimedomain,createdon=createdon)
                db.session.add(sinfo)
                db.session.commit()

                flash("New Schedule Record created successfully","success")
                return redirect(url_for('list_directory',directory_path=directory_path))
            
        except Exception as e:
            return {"error": f"Failed to save data: {str(e)}"}, 500
    else:
        return render_template('schedule_exam.html',form=form)

@app.route('/user/notification', methods=["GET", "POST"])
@login_required
def user_notification():
    # notifications = Schedule.query.order_by(Schedule.createdon).all()
    # print(notifications)
    db = get_db()
    sort_column = 'createdon'
    query = f"SELECT * FROM Schedule ORDER BY {sort_column}"
    cursor = db.execute(query)
    allnotifications = cursor.fetchall() 
    notifications = [dict(notific) for notific in allnotifications]
    return render_template('user_notification.html',notifications=notifications)

@app.route('/change_voice_language', methods=['POST'])
@login_required
@role_required('admin')
def change_voice_language():
    data = request.get_json()  # Get JSON data sent from JavaScript
    new_value = data.get('value')
    # Update your Flask variable or perform other server-side logic
    app.config['VOICE_LANGUAGE']= new_value
    return jsonify(message="Variable updated successfully")

# ROUTE : voice recognition (used by Admin)  
@app.route('/voice', methods=["GET", "POST"])
@login_required 
@role_required('admin') 
def voice():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`

            if app.config['VOICE_LANGUAGE'] == 'BENG':
                print(app.config['VOICE_LANGUAGE'])
                # sets voice language to bengali
                vtt = r.recognize_google(audio,language="bn-IN")
            else:
                print(app.config['VOICE_LANGUAGE'])
                # sets voice language to indian english
                vtt = r.recognize_google(audio,language="en-IN")  
            
            if vtt:
                api_data = {"vdata": vtt}
                flask_data = jsonify(api_data)
                return flask_data
            else:
                empty_dict = {}
                return empty_dict
            
           
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            # return redirect('/voice')
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            # return redirect('/voice')
            
# ROUTE : API to retrieve Class
@app.route('/api/get_studyClass')
@login_required
@role_required('admin')
def get_studyClass():
    db = get_db()
    cursor = db.execute('SELECT * FROM clClass')
    studyClasses = cursor.fetchall() 
    class_list_of_dict = [dict(studyClass) for studyClass in studyClasses]
    return jsonify(class_list_of_dict)     

# ROUTE : API to retrieve Semester
@app.route('/api/get_semester/<selected_class>')
@login_required
@role_required('admin')
def get_semester(selected_class):
    db = get_db()
    cursor = db.execute('SELECT * FROM Semester WHERE sm_class = ?', [selected_class])
    allsemester = cursor.fetchall() 
    semester_list_of_dict = [dict(semester) for semester in allsemester]
    return jsonify(semester_list_of_dict)           

# ROUTE : API to retrieve chapter
@app.route('/api/get_chapter/<selected_class>/<selected_sem>')
@login_required
@role_required('admin')
def get_chapter(selected_class,selected_sem):
    db = get_db()
    cursor = db.execute('SELECT * FROM Chapter WHERE ch_class = ? AND ch_sem = ?', [selected_class,selected_sem])
    allchapter = cursor.fetchall() 
    chapter_list_of_dict = [dict(chapter) for chapter in allchapter]
    return jsonify(chapter_list_of_dict)   

# ROUTE : API to retrieve Question Type
@app.route('/api/get_QuestionType')
@login_required
@role_required('admin')
def get_QuestionType():
    db = get_db()
    cursor = db.execute('SELECT * FROM Question_Type')
    QuestionTypes = cursor.fetchall() 
    QuestionType_list_of_dict = [dict(QuestionType) for QuestionType in QuestionTypes]
    return jsonify(QuestionType_list_of_dict)       
  
@app.route('/process-data/<examClass>/<examSem>/<examChapter>/<examQtype>', methods=['GET','POST'])
@login_required
@role_required('admin')
def process_data(examClass,examSem,examChapter,examQtype):
    selected_options = request.form.getlist('options')
    list_qids=[]
    for option in selected_options:
        list_qids.append(option)
        
    allQuestions = []
    for q in list_qids:
        id=int(q)
        question = Question_Bank.query.filter_by(id=id).all()
        #  converts each record into array of objects and then add it to dictionary object
        item = {
            'id': question[0].id,
            'studyclass' : question[0].studyclass,
            'sem' : question[0].sem,
            'chapter' : question[0].chapter,
            'questiontype' : question[0].parent_Question_Type.qtype_desc,
            'hasimage': question[0].hasimage, 
            'imagelocation': question[0].imagelocation,
            'question' : question[0].question, 
            'choices' : [question[0].op1,question[0].op2,question[0].op3,question[0].op4],
            'answer' : question[0].answer
            }
        allQuestions.append(item)
    
    data_to_save=allQuestions

    # create examinfo dictionary
    examinfo = []
    item = {'Class' : examClass,
            'Sem' : examSem,
            'Chapter' : examChapter,
            'QuestionType' : examQtype
            }
    examinfo.append(item)

    
    # save json object to json file
    # Specify the path to your JSON file
    basedir = os.path.abspath(os.path.dirname(__file__))
    datafile_path = os.path.join(basedir, 'static', 'Exam', 'data.json')
    exam_Infofile_path = os.path.join(basedir, 'static', 'Exam', 'ExamInfo.json')
    directory_path = os.path.join(basedir, 'static', 'Exam')  

    try:
        with open(datafile_path, 'w') as f:
            json.dump(data_to_save, f, indent=4) # indent for readability
            flash("Congratulation ... Question created successfully","success")

            with open(exam_Infofile_path,'w') as f:
                json.dump(examinfo, f, indent=4) # indent for readability
                flash("Congratulation ... Exam Info created successfully","success")

            return redirect(url_for('list_directory',directory_path=directory_path))
            
    except Exception as e:
            return {"error": f"Failed to save data: {str(e)}"}, 500

# ROUTE : to display user directory (only used by admin)
@app.route('/list_directory/<directory_path>')
@login_required
@role_required('admin')
def list_directory(directory_path):
    full_path = directory_path
    files_info = []

    if os.path.isdir(full_path):
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                mod_time_stamp = os.path.getmtime(item_path)
                mod_datetime = datetime.fromtimestamp(mod_time_stamp)
                files_info.append({
                    'name': item,
                    'size': size,
                    'modified': mod_datetime.strftime('%d-%m-%Y %H:%M:%S')
                })
        return render_template('directory_listing.html', files=files_info, directory=directory_path)
    else:
        return "Directory not found", 404

# ROUTE : to display user directory (only used by admin)
@app.route('/dir_listing')
@login_required
@role_required('admin')
def dir_listing():
    basedir = os.path.abspath(os.path.dirname(__file__))
    directory_path = os.path.join(basedir, 'static', 'Exam')  
    return redirect(url_for('list_directory',directory_path=directory_path))

# ROUTE : delete file from directory (only used by admin)
@app.route('/directory_listing/delete/<filename>')
@login_required
@role_required('admin')
def delete_file(filename):
    basedir = os.path.abspath(os.path.dirname(__file__))
    directory_path = os.path.join(basedir, 'static', 'Exam')  
    file_to_delete = os.path.join(directory_path, filename) 

    if os.path.exists(file_to_delete):
        try:
            os.remove(file_to_delete)
            flash("File deleted successfully.", "success")
        except Exception as e:
            flash("Error deleting file:", "warning")
        return redirect(url_for('dir_listing'))
    else:
        flash("File does not exist.", "danger")
        return redirect(url_for('dir_listing'))

# ROUTE : to display user directory (used by user)
@app.route('/user_list_directory/<directory_path>')
@login_required
def user_list_directory(directory_path):
    full_path = directory_path
    files_info = []

    if os.path.isdir(full_path):
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                mod_time_stamp = os.path.getmtime(item_path)
                mod_datetime = datetime.fromtimestamp(mod_time_stamp)
                files_info.append({
                    'name': item,
                    'size': size,
                    'modified': mod_datetime.strftime('%d-%m-%Y %H:%M:%S'),
                    'fullname': item_path
                })

        return render_template('user_directory_listing.html', files=files_info, directory=directory_path)
    else:
        return "Directory not found", 404

# ROUTE : to display user directory (used by user)
@app.route('/user/dir_listing')
@login_required
def user_dir_listing():
    basedir = os.path.abspath(os.path.dirname(__file__))
    directory_path = os.path.join(basedir, 'static', 'users', app.config['USERNAME'])  
    return redirect(url_for('user_list_directory',directory_path=directory_path))

# ROUTE : to display old user results (used by user)
@app.route('/user/oldresults/<filepath>')
@login_required
def user_oldresults(filepath):
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(basedir,'static','users',app.config['USERNAME'],filepath)
    print(filename)
    
    # read the content of JSON file stored in users home directory
    result = []
    try:
        with open(filename, 'r') as f:
            result = json.load(f)                                                
    except FileNotFoundError:
        return "Error: JSON File not found"
    except json.JSONDecodeError:
        return "Error: Error decoding JSON"     
    
    # separates ansermatix and examinfo
    ansmatrix = []
    examinfo = []
    
    for index, item in enumerate(result):
        if index <= len(result) - 2:
            ansmatrix.append(item)
        else:
            examinfo.append(item)
    
    total = 0
    obtscore = 0
 
    for ans in ansmatrix:
        total += 1
        if ans['cans'] == ans['qans']:
            obtscore += 1
    
    schstr = examinfo[0]['Schedule']
    
    # store the following for pdf creation
    app.config['ANSWER_MATRIX'] = ansmatrix
    examinfo = app.config['EXAM_INFO'] = examinfo
    app.config['TOTAL_MARKS'] = total
    app.config['OBTAINED_MARKS'] = obtscore
    app.config['SCHEDULE_INFO'] = schstr

    # fetch all records from question bank for question tooltip
    db = get_db()
    cursor = db.execute('SELECT * FROM Question_Bank')
    qb = cursor.fetchall() 
    qBank = [dict(q) for q in qb]

    isOldResult = [{"old":"Yes"}]
    
    return render_template('answerMatrix.html',ansmatrix=ansmatrix,qBank=qBank,examinfo=examinfo,isOldResult=isOldResult)   

@app.route('/create_question_set', methods=['GET','POST'])
@login_required
@role_required('admin')
def create_question_set():
    form=makeQuestionSet()
    basedir = os.path.abspath(os.path.dirname(__file__))
    destination_directory = os.path.join(basedir, 'static', 'Exam') 
    source_file = os.path.join(destination_directory, 'data.json')
    destination_file = os.path.join(destination_directory, 'set1.json')
    

    if request.method == "POST":
        setno = form.setno.data
        setalgo = form.setalgo.data
        
        # deletes old question sets
        file_pattern = "SET*.json" 
        if deleteAllFiles(destination_directory,file_pattern):
            flash("Old Question Sets deleted successfully","success")
        else:
            flash("Error Deleting Question Sets","warning")
            return redirect(url_for('dir_listing'))
        
        # creates multiple initial question set (copy the original data.json file)
        if fileCopy(setno,destination_directory,source_file):
            flash("New Question Set(s) created successfully","success")
        else:
            flash("Error copying file(s)","warning")
            return 
        
        # create multiple sets

        # get a list of all initial set files
        file_list = get_file_list(destination_directory,file_pattern)

        if file_list:
            for file_path in file_list:
                with open(file_path, 'r') as f:
                    data_read = json.load(f)
                    
                # flash("File loaded successfully","success")

                data_write = suffleQuestions(setalgo, data_read)

                with open(file_path, 'w') as f:
                    json.dump(data_write, f, indent=4)
                # flash("New Set created successfully","success")
        
        return redirect(url_for('dir_listing'))
    
    
    if fileExists(source_file):
        return render_template('create_question_set.html',form=form)
    else:
        flash("Source file does not exist or is not a file.","warning")
        return redirect(url_for('set_question'))

# ROUTE : API to store localstorage answer to flask global varible and then redirect to show score
@app.route('/score/api/process_answerMatrix_data', methods=['GET','POST'])
@login_required
def process_answerMatrix_data():
    if request.is_json:
        app.config['ANSWER_MATRIX'] = request.get_json()
        # Process the received JSON data here
        # print(f"Received JSON data: {answerMatrix}")

        # After processing, return a response that indicates a redirect
        # You can either return a status code and a redirect URL
        # or directly return a jsonify response with the redirect URL
        return jsonify({'message': 'Data processed successfully'})
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

# ROUTE : route to show score
@app.route('/score/<obtainedMarks>/<totalMarks>')
@login_required
def score(obtainedMarks,totalMarks):
    # stote score and total
    app.config['TOTAL_MARKS'] = totalMarks
    app.config['OBTAINED_MARKS'] = obtainedMarks

    scheduleinfo = app.config['SCHEDULE_INFO']

    # calculate % of marks
    om = float(obtainedMarks)
    tm = float(totalMarks)
    pm = round((om / tm * 100),2)
    fpm = str(pm)
   
    # update examstatus to reflect that user already submitted the exam
    update_examstatus = ExamStatus.query.filter_by(user_id=current_user.id,schedule=scheduleinfo).first()
    update_examstatus.exam_status = "Submitted"
    db.session.add(update_examstatus)
    db.session.commit()

    # update result table (add record)
    result = Result(user_id=current_user.id,schedule=scheduleinfo,marks=obtainedMarks,total=totalMarks,percentage=fpm) 
    db.session.add(result)
    db.session.commit()   

    # combined answer matrix and examinfo into one dictionary
    ansmatrix = app.config['ANSWER_MATRIX']
    examinfo = app.config['EXAM_INFO'] 
    
    data_to_save = []
    for row in ansmatrix:
        data_to_save.append(row)
    for row in examinfo:
        data_to_save.append(row)
    
    # save the combined dictionary into JSON file for later use
    basedir = os.path.abspath(os.path.dirname(__file__))
    home_directory = os.path.join(basedir, 'static','users',app.config['USERNAME'])  
    s1=scheduleinfo.replace("-","")
    s2=s1.replace(":","")
    s3=s2.replace(" ","")
    filename = "exam_" + s3 + ".json"
    fullFilePath = os.path.join(home_directory,filename)

    try:
        with open(fullFilePath, 'w') as f:
            json.dump(data_to_save, f, indent=4) # indent for readability
            # flash("","success")
    except Exception as e:
            return {"error": f"Failed to save data: {str(e)}"}, 500

    
    return render_template('scoreCard.html',obtainedMarks=obtainedMarks,totalMarks=totalMarks)   

# ROUTE : route to show answer matrix    
@app.route('/score/answermatrix')
@login_required
def answermatrix():
    db = get_db()
    cursor = db.execute('SELECT * FROM Question_Bank')
    qb = cursor.fetchall() 
    qBank = [dict(q) for q in qb]
    
    ansmatrix = app.config['ANSWER_MATRIX']
    examinfo = app.config['EXAM_INFO'] 
    isOldResult = [{"old":"No"}]
    return render_template('answerMatrix.html',ansmatrix=ansmatrix,qBank=qBank,examinfo=examinfo,isOldResult=isOldResult)   

# ROUTE : route to send email    
@app.route('/send_mail',methods=['GET','POST'])
@login_required
def send_mail():
    ansmatrix = app.config['ANSWER_MATRIX']
    examinfo = app.config['EXAM_INFO'] 
    total = app.config['TOTAL_MARKS']
    score = app.config['OBTAINED_MARKS']

    # retrieve the email of the current user
    user = User.query.filter_by(id=current_user.id).first()
    recipientEmail = user.email 
     
    subject = f"Scorecard of Exam on {examinfo[0]['Schedule']}"
    msg = Message(subject=subject,recipients=[recipientEmail])
    # render the email template
    msg.html = render_template('email_template.html', ansmatrix=ansmatrix, examinfo=examinfo, total=total, score=score)
    
    try:
        mail =  mailSetup()
        mail.send(msg)
        flash(f"Email sent successfully", "success")
        # redirect to send SMS
        return redirect(url_for('send_sms'))
    except Exception as e:
        flash(f"Error Sending email : {str(e)}", "error")
        return redirect(url_for('send_sms'))
    
@app.route('/send_sms', methods=['GET','POST'])
@login_required
def send_sms():
    ACCOUNT_SID=os.getenv('ACCOUNT_SID')
    AUTH_TOKEN=os.getenv('AUTH_TOKEN')
    TWILIO_NUMBER=os.getenv('TWILIO_NUMBER')
    to_mobile_number = "+919434229166"

    if not ACCOUNT_SID or not AUTH_TOKEN or not TWILIO_NUMBER:
        flash("Twilio credentials are not configured.", "error")
        return redirect(url_for('dashboard_user'))

    try:       
        totalMarks = app.config['TOTAL_MARKS']
        obtainedMarks = app.config['OBTAINED_MARKS']
        scheduleinfo = app.config['SCHEDULE_INFO']
        
        date_format = "%Y-%m-%d %H:%M:%S" 
        fmt_scheduleinfo = datetime.strptime(scheduleinfo, date_format)
        formatted_scheduleinfo = fmt_scheduleinfo.strftime("%d-%m-%Y %H:%M:%S")

        message_body = f"Result of Exam Conducted on {formatted_scheduleinfo} : You Score is {obtainedMarks} out of {totalMarks}"
        
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=to_mobile_number,
            from_=TWILIO_NUMBER,
            body=message_body
        )
        flash(f"SMS sent successfully to {to_mobile_number}! Message SID: {message.sid}", "success")
        return redirect(url_for('send_whatsapp_message'))
    
    except Exception as e:
        flash(f"Error sending SMS: {e}", "error")
        print(e)
        return redirect(url_for('send_whatsapp_message'))
    
    
@app.route('/send_whatsapp', methods=['GET','POST'])
@login_required
def send_whatsapp_message():
    ACCOUNT_SID=os.getenv('ACCOUNT_SID')
    AUTH_TOKEN=os.getenv('AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER=os.getenv('TTWILIO_WHATSAPP_NUMBER')
    to_mobile_number = "+919434229166"

    if not ACCOUNT_SID or not AUTH_TOKEN or not TWILIO_WHATSAPP_NUMBER:
        flash("Twilio credentials are not configured.", "error")
        return redirect(url_for('dashboard_user'))

    try:       
        totalMarks = app.config['TOTAL_MARKS']
        obtainedMarks = app.config['OBTAINED_MARKS']
        scheduleinfo = app.config['SCHEDULE_INFO']
        
        date_format = "%Y-%m-%d %H:%M:%S" 
        fmt_scheduleinfo = datetime.strptime(scheduleinfo, date_format)
        formatted_scheduleinfo = fmt_scheduleinfo.strftime("%d-%m-%Y %H:%M:%S")

        message_body = f"Result of Exam Conducted on {formatted_scheduleinfo} : You Score is {obtainedMarks} out of {totalMarks}"
        
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER, 
                body=message_body,
                to=f'whatsapp:{to_mobile_number}'
            )
       
        flash(f"Whatsapp Message sent successfully to {to_mobile_number}! Message SID: {message.sid}", "success")
        return redirect(url_for('dashboard_user'))
    
    except Exception as e:
        flash(f"Error sending SMS: {e}", "error")
        print(e)
        return redirect(url_for('dashboard_user'))

# (NOW NOT USING ) used to create pdf only using xhtml2pdf
@app.route('/create_pdf', methods=['GET','POST'])
@login_required
def create_pdf():
#     ansmatrix = app.config['ANSWER_MATRIX']
#     examinfo = app.config['EXAM_INFO'] 
#     total = app.config['TOTAL_MARKS']
#     score = app.config['OBTAINED_MARKS']
    
#     # Define your HTML content
#     html_content = render_template('pdf_template.html', ansmatrix=ansmatrix, examinfo=examinfo, total=total, score=score)

#     # Open a file for writing the PDF
#     with open("output.pdf", "wb") as pdf_file:
#         # Convert HTML to PDF
#         pisa_status = pisa.CreatePDF(
#                 html_content,    # the HTML to convert
#                 dest=pdf_file)   # file handle to receive result

#     # Check if PDF creation was successful
#     if not pisa_status.err:
#         print("PDF created successfully!")
#     else:
#         print("Error creating PDF:", pisa_status.err)
    
    return ""

# (NOW NOT USING ) used to create & download pdf without saving using reportlab
@app.route('/download_pdf', methods=['GET','POST'])
@login_required
def download_pdf():
#     ansmatrix = app.config['ANSWER_MATRIX']
#     examinfo = app.config['EXAM_INFO'] 
#     total = app.config['TOTAL_MARKS']
#     score = app.config['OBTAINED_MARKS']
    
#     # Define your HTML content
#     html_content = render_template('pdf_template.html', ansmatrix=ansmatrix, examinfo=examinfo, total=total, score=score)
    
#     # 1. Generate the PDF in-memory
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#     p.drawString(100, 750, html_content)
#     p.showPage()
#     p.save()

#     # 2. Prepare the response for download
#     buffer.seek(0)  # Rewind the buffer to the beginning
#     return send_file(
#         buffer,
#         mimetype='application/pdf',
#         as_attachment=True,
#         download_name='my_dynamic_document.pdf'
#     )
      return ""

# create & download pdf without saving on server
@app.route('/generate_pdf')
@login_required
def generate_pdf():
    # Prepare data for the template
    ansmatrix = app.config['ANSWER_MATRIX']
    examinfo = app.config['EXAM_INFO'] 
    total = app.config['TOTAL_MARKS']
    score = app.config['OBTAINED_MARKS']
    sch = app.config['SCHEDULE_INFO']
    
    # generate pdf filename
    date_format = "%Y-%m-%d %H:%M:%S" 
    fmt_scheduleinfo = datetime.strptime(sch, date_format)
    formatted_scheduleinfo = fmt_scheduleinfo.strftime("%d-%m-%Y %H:%M:%S")
    s1=formatted_scheduleinfo.replace("-","")
    s2=s1.replace(" ","")
    s3=s2.replace(":","")
    pdfFileName=s3 + ".pdf"
    # context = {'name': name, 'date': date.today().strftime("%B %d, %Y")}

    # Define your HTML content
    html_content = render_template('pdf_template.html', ansmatrix=ansmatrix, examinfo=examinfo, total=total, score=score)

    # Create a file-like object to store the PDF
    pdf_buffer = io.BytesIO()

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html_content,                # the HTML to convert
        dest=pdf_buffer)     # file handle to receive result

    # Check if PDF creation was successful
    if pisa_status.err:
        return "Failed to generate PDF", 500

    # Prepare the response for download
    pdf_buffer.seek(0)  # Rewind the buffer to the beginning
    response = make_response(pdf_buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={pdfFileName}'
    return response

# Displays student performence
@app.route('/perfommence')
@login_required
def perfommence():
    # retrieve the records of the current user from result table
    db = get_db()
    cursor = db.execute('SELECT * FROM Result where user_id = ?', [current_user.id])
    rslt = cursor.fetchall() 
    result = [dict(r) for r in rslt]
     
    return render_template('performence.html',result=result)   

# ROUTE : logout
@app.route('/get_email')
def get_email():
    form = getEmail()
    return render_template('get_email.html', form=form)

# ROUTE : Forgot Password
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')  # Get email from the form input
    
    if not email:
        flash('Please enter your email address first.', "danger")
        return redirect(url_for('get_email'))

    # Check if email exists in the database
    db = get_db()
    cursor = db.execute("SELECT * FROM User WHERE email = ?", [email])
    userdata = cursor.fetchone()
    
    if not userdata:
        flash('Email not found! Please check and try again.', "danger")
        return redirect(url_for('get_email'))

    try:
        # Generate Reset Token
        token = generate_reset_token(email)
        reset_link = url_for('reset_password', token=token, _external=True)

        # Send Email
        msg = Message('Password Reset Request', sender='pradiptahalder2023@gmail.com.com', recipients=[email])
        msg.body = f'Click the link to reset your password: {reset_link}'
        mail =  mailSetup()
        mail.send(msg)

        flash('Password reset link has been sent to your email!', "success")
    except Exception as e:
        print(e)
        flash('An error occurred while sending email. Please try again.', "danger")

    return redirect(url_for('get_email'))  # Redirect to login page after sending email

# ROUTE : Reset Password
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('Invalid or expired token', "danger")
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirmpassword']

        repatcha_response = request.form.get('g-recaptcha-response')

        # captcha verification
        data = {
            'secret':os.getenv('RECAPTCHA_SECRET_KEY'),
            'response':repatcha_response
        }
        
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
        result = r.json()
                
        if not result.get('success'):
            flash("Captcha failed. Please try again.","danger")
            return redirect(url_for('reset_password',token=str(token)))


        if new_password != confirm_password:
            flash('Passwords do not match!', "danger")
            return redirect(url_for('reset_password', token=token))

        hashed_password = generate_password_hash(new_password)

        # Update password in the database
        db = get_db()
        cursor = db.execute("UPDATE User SET password = ? WHERE email = ?", [hashed_password, email])
        db.commit()
        

        flash('Your password has been updated!', "success")
        return redirect(url_for('login'))

    form = forgotPasswordForm()
    site_key = os.getenv('RECAPTCHA_SITE_KEY')
    return render_template('reset_password.html', form=form, token=token, site_key=site_key)  # ✅ Pass token to template

# ROUTE : Change Password Route
@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    if request.method == 'POST':

        # captcha verification
        repatcha_response = request.form.get('g-recaptcha-response')
        
        data = {
            'secret':os.getenv('RECAPTCHA_SECRET_KEY'),
            'response':repatcha_response
        }
        
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
        result = r.json()
        
        if not result.get('success'):
            flash("Captcha failed. Please try again.","danger")
            return redirect(url_for('change_password'))
        

        current_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        confirm_password = request.form['confirmnewpassword']

        db = get_db()
        cursor = db.execute("SELECT * FROM User WHERE id = ?", [current_user.id])
        userdata = cursor.fetchone()

        #Check if password is correct
        if not check_password_hash(userdata['password'], current_password):
            flash('Current password is incorrect!', "danger")
            return redirect(url_for('change_password'))
        
        if new_password != confirm_password:
            flash('New passwords do not match!', "danger")
            return redirect(url_for('change_password'))

        # Update password in the database
        hashed_password = generate_password_hash(new_password)
        db = get_db()
        cursor = db.execute("UPDATE User SET password = ? WHERE id = ?", [hashed_password, current_user.id])
        db.commit()

        flash('Your password has been changed successfully!', "success")
        return redirect(url_for('logout'))

    form = changePasswordForm()
    site_key = os.getenv('RECAPTCHA_SITE_KEY')
    return render_template('change_password.html', form=form, site_key=site_key)

# ROUTE : User Profile Route
@app.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    # retrieve the records of the current user from User table
    userdata = User.query.filter_by(id=current_user.id).first()
    
    # retrieve the records of the current user from result table
    # db = get_db()
    # cursor = db.execute('SELECT * FROM Result where user_id = ?', [current_user.id])
    # rslt = cursor.fetchall() 
    # result = [dict(r) for r in rslt]

    # calculate performence average 
    result = Result.query.filter_by(user_id=current_user.id).all()
    if result:
        sum = 0.0
        i = 0
        for r in result:
            i = i + 1
            sum = sum + float(r.percentage)
        avgp = sum / i
    else:
        # if no result data is found
        avgp = 0.00
    
    return render_template('user_profile.html',userdata=userdata,avgp=avgp)

@app.route('/updatePhone/<device>/<mode>', methods=['GET', 'POST'])
def updatePhone(device,mode):
    form = PhoneForm()
    if form.validate_on_submit():
        phoneno = form.phone.data

        if device == "mobile" :
            userdata = User.query.filter_by(id=current_user.id).first()
            userdata.mobileno = phoneno
            db.session.add(userdata)
            db.session.commit()
            flash("Phone Number has been updated Successfully","success")
            return redirect(url_for('user_profile'))
        
        if device == "whatsapp" :
            userdata = User.query.filter_by(id=current_user.id).first()
            userdata.whatsappno = phoneno
            db.session.add(userdata)
            db.session.commit()
            flash("whatsapp Number has been updated Successfully","success")
            return redirect(url_for('user_profile'))
        
    return render_template('updatePhone.html', form=form, device=device,mode=mode)

# ROUTE : google auth request
@app.route('/google')
def google():
    # Redirect to google_auth function
    try:
        redirect_uri = url_for('google_auth', _external=True)
        session['nonce'] = generate_token()
        return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])
    except Exception as e:
        app.logger.error(f"Error during login:{str(e)}")
        return f"Error occurred during login{str(e)}",500

# ROUTE : google auth reponse and login
@app.route('/google/auth')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])

    # print(user)

    # Get the Google user's email amd username
    google_username = user['name']
    google_email = user['email']
    google_picture = user['picture']
        
    # Find or create a user in your local database
    user = User.query.filter_by(email=google_email).first()
    
    if not user:
        # Create a new user if they don't exist
        username = google_email.split('@')[0]
       
        user = User(
            username = username,
            password = generate_password_hash(google_email),
            email = google_email,
            createdon = datetime.now(),
            updatedon = datetime.now()
            )
        db.session.add(user)
        db.session.commit()

         # create users home directory
        basedir = os.path.abspath(os.path.dirname(__file__))
        directory_path = os.path.join(basedir, 'static', 'users') 

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        
        home_directory = os.path.join(directory_path,username)

        if not os.path.exists(home_directory):
            os.makedirs(home_directory)
        
    session['oauth_token'] = token
    session['username'] = google_email

    # set the username in app.config
    app.config['USERNAME']=google_email.split('@')[0]
    app.config['PROFILEPIC']=str(google_picture)

    # Log the custom User object into Flask-Login
    login_user(user)
    flash("Logged in Successfully","success")
    return redirect(url_for('dashboard_user'))

# ROUTE : facebook auth request
# @app.route('/faebook')
# def facebook():
#     if not facebook.authorized:
#         return redirect(url_for("facebook.login"))
    
#     # If the user is authorized, fetch their profile data
#     resp = facebook.get("/me?fields=id,name,email")
#     assert resp.ok, resp.text
    
#     # Display a message with the user's name
#     name = resp.json()["name"]
#     return f"You are logged in as: {name}"


@app.route('/login/twitter')
def login_twitter():
    return twitter.authorize_redirect(redirect_uri=url_for('callback_twitter', _external=True))

@app.route('/callback/twitter')
def callback_twitter():
    token = twitter.authorize_access_token()
    # Store the token securely (e.g., in a database associated with the user)
    # You can now use this token to make API requests to Twitter on behalf of the user
    user_info = twitter.get('users/me', token=token).json()
    return f"Hello, {user_info['data']['name']}! Your Twitter ID is {user_info['data']['id']}"


# ROUTE : logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out Successfully","success")
    return redirect(url_for('login'))

# for error handling
@app.errorhandler(404)
def not_found_page(error):
    return render_template('errors/404.html'),404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/404.html'),500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)