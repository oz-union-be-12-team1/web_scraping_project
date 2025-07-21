from flask import Flask, Blueprint, jsonify, abort, request
from config import db
from app.models import Choices, Question, Answer
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
@choices_blp.route('/update/<int:choice_id>', methods=["PUT"])
def update_choice(choice_id):
    up_choice = Choices.query.get(choice_id)
    if not up_choice:
        return jsonify({"message" : "해당 질문이 없습니다."}), 404
    
    data = request.get_json()

    for field in ['content', 'is_active', 'sqe', 'question_id']:
        if field in data:
            setattr(up_choice, field, data[field])

    up_choice.update_at = datetime.now()
    db.session.commit()

    return jsonify({
        "id" : up_choice.id,
        "question_id" : up_choice.question_id,
        "content" : up_choice.content,
        "sqe" : up_choice.sqe,
        "is_active" : up_choice.is_active
    })

# 선택지 삭제
@choices_blp.route('/delete/<int:choice_id>', methods=["DELETE"])
def delete_choice(choice_id):
    del_choice = Choices.query.get(choice_id)
    if not del_choice:
        return jsonify({"message" : "해당 질문이 없습니다."}), 404
    
    answers = Answer.query.filter_by(choice_id=choice_id).first()
    if answers:
        return jsonify({"message" : "answer이 있어 선택지를 삭제할 수 없습니다."}), 400
    
    db.session.delete(del_choice)
    db.session.commit()
    
    return jsonify({"message" : f"id : {choice_id} 질문 삭제완료 했습니다"})
