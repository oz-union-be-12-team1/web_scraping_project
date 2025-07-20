from config import db
from datetime import datetime, timedelta, timezone
from enum import Enum

KST = timezone(timedelta(hours=9))

def now_kst():
    return datetime.now(KST)

# 정해진 값중 선택을 해야할 경우 사용함 --> 질문지도 고정되면 ENUM 쓰는게 좋을것같은데? --> 관리자에 의해 변경될수 있으므로 안씀

class Age(Enum):
    TEEN = 'teen'
    TWENTY = 'twenty'
    THIRTY = 'thirty'
    FORTY = 'forty'
    FIFTY = 'fifty'

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'

class ImageType(Enum):
    MAIN = 'main'
    SUB = 'sub'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Enum(Age), nullable=False)
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

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(ImageType), nullable=False)
    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)

    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=True)
    image = db.relationship('Image', backref='questions', lazy=True)

    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)

    choices = db.relationship('Choices', backref='question', lazy=True)

class Choices(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=now_kst)
    updated_at = db.Column(db.DateTime, default=now_kst, onupdate=now_kst)

    answers = db.relationship('Answer', backref='choice', lazy=True)

