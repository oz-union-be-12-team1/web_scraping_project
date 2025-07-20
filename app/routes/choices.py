from flask import Flask, Blueprint, jsonify, abort, request
from config import db
from app.models import Choices, Question
from datetime import datetime

choices_blp = Blueprint("choices", __name__, url_prefix='/choice')

# 선택지 생성
@choices_blp.route('', methods=['POST'])
def create_choice():
    data = request.get_json()

    if not all(data.get(field) for field in ['question_id', 'content', 'sqe']):
        return jsonify({"error" : "question_id, content, sqe 중 값이 없는 게 있습니다. 다시 확인해 주세요." }), 400

    new_choice = Choices(
        question_id=data['question_id'],
        content=data['content'],
        sqe=data['data'],
        is_active=True
    ) 

    db.session.add(new_choice)
    db.session.commit()

    return jsonify({
        "id" : new_choice.id,
        "question_id" : new_choice.question_id,
        "content" : new_choice.content,
        "sqe" : new_choice.sqe,
        "is_active" : new_choice.is_active
    })

# 선택지 수정
@choices_blp.route('/update/<int:choice_id>', methods=["GET","POST"])
def update_choice(choice_id):
    update_choice = Choices.query.get(choice_id)
    if not update_choice:
        return jsonify({"message" : "해당 질문이 없습니다."}), 404
    
    data = request.get_json()

    for field in ['content', 'is_active', 'sqe', 'question_id']:
        if field in data:
            setattr(update_choice, field, data[field])

    update_choice.update_at = datetime.utcnow()
    update_choice.session.commit()

    return jsonify({
        "id" : update_choice.id,
        "question_id" : update_choice.question_id,
        "content" : update_choice.content,
        "sqe" : update_choice.sqe,
        "is_active" : update_choice.is_active
    })

