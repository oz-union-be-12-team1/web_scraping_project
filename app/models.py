from config import db

class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    image_id = db.Column(db.Integer, db.ForeignKey('image_id'), nullable=False)

class Choices(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    question_id = db.Column(db.Integer, db.ForeignKey('question_id'), nullable=False)
