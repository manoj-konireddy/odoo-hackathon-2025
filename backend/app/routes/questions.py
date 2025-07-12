from flask import Blueprint, request
from app import mysql
from app.utils import response

questions_bp = Blueprint('questions', __name__)


@questions_bp.route('/with-answers', methods=['GET'])
def get_questions_with_answers():
    try:
        cur = mysql.connection.cursor()

        # Fetch all questions and their author
        cur.execute("""
            SELECT q.id, q.title, q.description, q.created_at, u.username
            FROM questions q
            JOIN users u ON q.user_id = u.id
            ORDER BY q.created_at DESC
        """)
        questions = cur.fetchall()

        result = []
        for q in questions:
            question_id = q["id"]
            # Fetch answers for this question
            cur.execute("""
                SELECT a.content, a.created_at, u.username
                FROM answers a
                JOIN users u ON a.user_id = u.id
                WHERE a.question_id = %s
                ORDER BY a.created_at ASC
            """, (question_id,))
            answers = cur.fetchall()

            result.append({
                "id": question_id,
                "title": q["title"],
                "description": q["description"],
                "author": q["username"],
                "created_at": q["created_at"].strftime("%Y-%m-%d %H:%M"),
                "answers": [{
                    "content": ans["content"],
                    "author": ans["username"],
                    "created_at": ans["created_at"].strftime("%Y-%m-%d %H:%M")
                } for ans in answers]
            })

        cur.close()
        return response(data=result)

    except Exception as e:
        print("🔥 Error loading questions with answers:", e)
        return response(success=False, message="Failed to fetch data"), 500


@questions_bp.route('/', methods=['GET'])
def get_questions():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT q.id, q.title, q.description, u.username
        FROM questions q
        JOIN users u ON q.user_id = u.id
        ORDER BY q.created_at DESC
    """)
    questions = cur.fetchall()
    cur.close()

    return response(data=[{
        "id": q["id"],
        "title": q["title"],
        "description": q["description"],
        "author": q["username"]
    } for q in questions])


@questions_bp.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    title = data['title']
    description = data['description']
    user_id = data['user_id']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO questions (user_id, title, description) VALUES (%s, %s, %s)",
                (user_id, title, description))
    mysql.connection.commit()
    cur.close()

    return response(message="Question posted")


@questions_bp.route('/tags', methods=['GET'])
def get_tags():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT name FROM tags LIMIT 20")
        rows = cur.fetchall()
        cur.close()

        tags = [{"name": row[0]} for row in rows]
        return response(data=tags)
    except Exception as e:
        print("Tags route error:", e)
        return response(success=False, message="Failed to fetch tags"), 500
