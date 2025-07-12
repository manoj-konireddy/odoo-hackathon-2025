from flask import Blueprint, request, jsonify
from backend.main import db
from models.answer import Answer
from datetime import datetime

answers_bp = Blueprint('answers', __name__)

# Submit an answer


@answers_bp.route('/submit', methods=['POST'])
def submit_answer():
    data = request.json
    content = data.get('content')
    user_id = data.get('user_id')
    question_id = data.get('question_id')

    if not content or not user_id or not question_id:
        return jsonify({'error': 'content, user_id, and question_id are required'}), 400

    answer = Answer(
        content=content,
        user_id=user_id,
        question_id=question_id,
        timestamp=datetime.utcnow()
    )

    db.session.add(answer)
    db.session.commit()

    return jsonify({'message': 'Answer submitted successfully'}), 201

# Get all answers for a question


@answers_bp.route('/<int:question_id>', methods=['GET'])
def get_answers(question_id):
    answers = Answer.query.filter_by(question_id=question_id).order_by(
        Answer.timestamp.desc()).all()
    result = []

    for ans in answers:
        result.append({
            'id': ans.id,
            'content': ans.content,
            'votes': ans.votes,
            'is_accepted': ans.is_accepted,
            'timestamp': ans.timestamp.isoformat(),
            'user_id': ans.user_id,
            'question_id': ans.question_id
        })

    return jsonify(result)

# Upvote or downvote an answer


@answers_bp.route('/vote', methods=['POST'])
def vote_answer():
    data = request.json
    answer_id = data.get('answer_id')
    vote_type = data.get('vote')  # 'up' or 'down'

    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({'error': 'Answer not found'}), 404

    if vote_type == 'up':
        answer.votes += 1
    elif vote_type == 'down':
        answer.votes -= 1
    else:
        return jsonify({'error': 'Invalid vote type'}), 400

    db.session.commit()
    return jsonify({'message': 'Vote recorded', 'votes': answer.votes})

# Mark an answer as accepted


@answers_bp.route('/accept', methods=['POST'])
def accept_answer():
    data = request.json
    answer_id = data.get('answer_id')

    answer = Answer.query.get(answer_id)
    if not answer:
        return jsonify({'error': 'Answer not found'}), 404

    # Reset any previously accepted answers for this question
    Answer.query.filter_by(question_id=answer.question_id).update(
        {'is_accepted': False})

    answer.is_accepted = True
    db.session.commit()
    return jsonify({'message': 'Answer marked as accepted'})
