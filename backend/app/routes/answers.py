from flask import Blueprint, request
from app import mysql
from app.utils import response

answers_bp = Blueprint('answers', __name__)


@answers_bp.route('/<int:question_id>', methods=['GET'])
def get_answers(question_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT a.content, u.username FROM answers a JOIN users u ON a.user_id = u.id WHERE a.question_id = %s", (question_id,))
    result = cur.fetchall()
    cur.close()

    answers = [{"content": a[0], "author": a[1]} for a in result]
    return response(data=answers)


@answers_bp.route('/add', methods=['POST'])
def add_answer():
    data = request.json
    content = data['content']
    user_id = data['user_id']
    question_id = data['question_id']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO answers (question_id, user_id, content) VALUES (%s, %s, %s)",
                (question_id, user_id, content))
    mysql.connection.commit()
    cur.close()

    return response(message="Answer added")


@answers_bp.route('/accept/<int:answer_id>', methods=['POST'])
def accept_answer(answer_id):
    data = request.json
    user_id = data.get('user_id')

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT q.user_id FROM questions q
        JOIN answers a ON q.id = a.question_id
        WHERE a.id = %s
    """, (answer_id,))
    owner = cur.fetchone()

    if owner and owner['user_id'] == user_id:
        cur.execute(
            "UPDATE answers SET is_accepted = TRUE WHERE id = %s", (answer_id,))
        mysql.connection.commit()
        cur.close()
        return response(message="Answer accepted.")
    else:
        cur.close()
        return response(success=False, message="Not authorized."), 403
