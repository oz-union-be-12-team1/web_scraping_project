from flask import Flask, Blueprint, jsonify, request
from config import db
from app.models import Choices, Question
from datetime import datetime
questions_blp = Blueprint('questions', __name__, url_prefix='/quesions')

# 특정 질문 가져오기
@questions_blp.route('/<int:question_sqe>', methods = ['GET'])
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
@questions_blp.route('/count', method=['GET'])
def count_question():
    total = Question.query.count()

    return jsonify({"total" : total})

# 질문 생성
@questions_blp.route('/create', methods=['POST'])
def create_question():
    data = request.get_json()

    if not all(data.get(field) for field in ['image_id', 'title', 'sqe', 'is_active']):
        return jsonify({'error' : 'image_id, title, sqe, is_active 중 값이 없는게 있습니다. 다시 확인해 주세요.'}),  400
    
    new_question = Question(
        image_id = data['image_id'],
        title = data['title'],
        sqe = data['sqe'],
        is_active = True
    )

    db.session.add(new_question)
    db.session.commit()

    return jsonify({"id" : new_question.id,
        "question_id" : new_question.question_id,
        "content" : new_question.content,
        "sqe" : new_question.sqe,
        "is_active" : new_question.is_active})

# 질문 수정
@questions_blp.route('/update/<int:question_id>', methods=["PUT"])
def update_question(quesstion_id):
    up_question = Question.query.get(quesstion_id)
    if not up_question:
        return jsonify({"message" : "해당 질문이 없습니다."}), 404
    
    data = request.get_json()

    for field in ['image_id', 'title', 'sqe']:
         if field in data:
             setattr(up_question, field, data[field])

    up_question.update_at = datetime.now()
    db.session.commit()

    return jsonify({"id" : up_question.id,
        "question_id" : up_question.question_id,
        "content" : up_question.content,
        "sqe" : up_question.sqe,
        "is_active" : up_question.is_active})

# 질문 삭제
@questions_blp.route('/delete/<int:question_id>', methods=["DELETE"])
def delete_question(question_id):
    del_question = Question.query.get(question_id)
    
    if not del_question:
        return jsonify({"message" : "해당 질문이 없습니다."}), 404
    
    choice = Choices.query.filter_by(question_id=question_id).first()
    
    if choice:
        return jsonify({"message" : "선택지가 있어 삭제할수 없습니다."}), 400
    
    db.session.delete(del_question)
    db.session.commit()

    return jsonify({"message" : f"id : {question_id} 질문 삭제완료 했습니다."})