from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from enum import Enum as PyEnum # 이름변경함 향후 이질문지가 바뀔수 있으므로, sql Enum과 혼동되지 않도록 이름 변경함

db = SQLAlchemy()

KST = timezone(timedelta(hours=9))

def now_kst():
    return datetime.now(KST)

# 정해진 값중 선택을 해야할 경우 사용함 --> 질문지도 고정되면 ENUM 쓰는게 좋을것같은데? --> 관리자에 의해 변경될수 있으므로 안씀

class Age(PyEnum):
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


