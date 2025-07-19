from flask import Flask, Blueprint, jsonify, request
from config import db
from app.models import Choices, Question

questions_bp = Blueprint('questions', __name__, url_prefix='/quesions')

# 특정 질문 가져오기
@questions_bp.route('/<int:question_sqe>', methods = ['GET'])
def get_question(question_sqe):

    question = Question.query.filter_by(sqe = question_sqe).first()

    if not question:
       return jsonify({"message" : "question을 찾을수가 없습니다."}), 404

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
