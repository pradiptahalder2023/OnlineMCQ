from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='guest')
    email = db.Column(db.String(150), nullable=False)
    createdon = db.Column(db.DateTime, default=datetime.now())
    updatedon = db.Column(db.DateTime, default=datetime.now())
    mobileno = db.Column(db.String(20), nullable=True)
    whatsappno = db.Column(db.String(20), nullable=True)

    
class clClass(UserMixin,db.Model):
    __tablename__ = 'clClass'

    id = db.Column(db.Integer, primary_key=True)
    cl_desc = db.Column(db.String(100), nullable=False)

class Question_Type(UserMixin,db.Model):
    __tablename__ = 'Question_Type'

    id = db.Column(db.Integer, primary_key=True)
    qtype_desc = db.Column(db.String(100), nullable=False)

    # Define the relationship to the Child model (Question_Bank)
    # 'children_Question_Bank' is the name of the attribute on Parent to access children (Question_Bank)
    # back_populates='parent_Question_Type' creates the reverse relationship on Child
    children_Question_Bank = db.relationship('Question_Bank', back_populates='parent_Question_Type', lazy=True)

class Question_Bank(UserMixin, db.Model):
    __tablename__ = 'Question_Bank'

    id = db.Column(db.Integer, primary_key=True)
    studyclass = db.Column(db.String(2), nullable=False)
    sem = db.Column(db.String(2), nullable=False)
    hasimage = db.Column(db.String(2), nullable=True)
    imagelocation = db.Column(db.String(200), nullable=True)
    chapter=db.Column(db.String(2), nullable=True)
    question = db.Column(db.String(200), nullable=False)
    op1 = db.Column(db.String(200), nullable=False)
    op2 = db.Column(db.String(200), nullable=False)
    op3 = db.Column(db.String(200), nullable=False)
    op4 = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    
    # Define the foreign key linking to the Parent (Question_Type)
    Question_Type_id = db.Column(db.Integer, db.ForeignKey('Question_Type.id'), nullable=False)
    # Define the relationship back to the Parent (Question_Type)
    # 'parent_Question_Type' is the name of the attribute on Child (Question_Bank) to access the parent (Question_Type)
    parent_Question_Type = db.relationship('Question_Type', back_populates='children_Question_Bank')

class Chapter(UserMixin, db.Model):
    __tablename__ = 'Chapter'
    id = db.Column(db.Integer, primary_key=True)
    ch_class = db.Column(db.String(100), nullable=False)
    ch_sem = db.Column(db.String(100), nullable=False)
    ch_no = db.Column(db.String(2), nullable=False)
    ch_desc = db.Column(db.String(100), nullable=False)

class Semester(UserMixin, db.Model):
    __tablename__ = 'Semester'
    id = db.Column(db.Integer, primary_key=True)
    sm_class = db.Column(db.String(100), nullable=False)
    sm_desc = db.Column(db.String(100), nullable=False)

class ExamStatus(UserMixin, db.Model):
    __tablename__ = 'ExamStatus'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(10), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    set_name = db.Column(db.String(100), nullable=False)
    exam_status = db.Column(db.String(100), nullable=False)

class Result(UserMixin, db.Model):
    __tablename__ = 'Result'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.String(10), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.String(100), nullable=False)
    total = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.String(100), nullable=False)

class Schedule(UserMixin, db.Model):
    __tablename__ = 'Schedule'
    id = db.Column(db.Integer,primary_key=True)
    studyclass = db.Column(db.String(10), nullable=False)
    sem = db.Column(db.String(100), nullable=False)
    chapter = db.Column(db.String(100), nullable=False)
    qtype = db.Column(db.String(100), nullable=False)
    sch = db.Column(db.String(100), nullable=False)
    examduration = db.Column(db.String(100), nullable=False)
    examtimedomain = db.Column(db.String(100), nullable=False)
    createdon = db.Column(db.DateTime, nullable=False)

       
        