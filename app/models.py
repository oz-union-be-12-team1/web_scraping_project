from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from enum import Enum as PyEnum

db = SQLAlchemy()

KST = timezone(timedelta(hours=9))

def now_kst():
    return datetime.now(KST)

# --- Enums ---(정해진 값중 선택을 해야할 경우 사용함) --> 질문지도 고정되면 ENUM 쓰는게 좋을것같은데? --> 관리자에 의해 변경될수 있으므로 안씀

class AgeGroup(PyEnum):
    TEEN = 'teen'
    TWENTY = 'twenty'
    THIRTY = 'thirty'
    FORTY = 'forty'
    FIFTY = 'fifty'

class Gender(PyEnum):
    MALE = 'male'
    FEMALE = 'female'

class ImageType(PyEnum):
    MAIN = 'main'
    SUB = 'sub'

# --- Models ---
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Enum(AgeGroup), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)

    answers = db.relationship('Answer', backref='user', lazy=True)


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)


class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)

    answers = db.relationship('Answer', backref='choice', lazy=True)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)

    choices = db.relationship('Choice', backref='question', lazy=True)


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(ImageType), nullable=False)
    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)