from flask import Flask, Blueprint, jsonify, abort, request
from config import db
from app.models import Choices, Question

app = Flask(__name__)

questions_bp = Blueprint('questions', __name__, url_prefix='/quesions')

# 특정 질문 가져오기
@questions_bp.route('/<int:question_sqe>', methods = ['GET'])
def get_question(question_sqe):

    question = Question.query.filter_by(sqe = question_sqe).first()

    if not question:
        abort(400, discription="없는 질문 순번입니다.")

    choices = Choices.query.filter_by(question_id=question.id).all()

    return jsonify({
        "id": question.id,
        "title": question.title,
        "image": question.image_id,
        "choices": [
            {
                "id": choice.id,
                "content": choice.content,
                "is_active": choice.is_active,
                "sqe": choice.sqe,
                "question_id": choice.question_id
            }
            for choice in choices
        ]
    })   

# 질문 개수 확인
@questions_bp.route('/count', method=['GET'])
def count_question():
    total = Question.query.count()

    return jsonify({"total" : total})

if __name__ == '__main__':
    app.run(debug=True)