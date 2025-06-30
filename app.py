from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import db  

# Database setup
db.create_user_table()
db.create_task_table()

# Flask setup
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'berfin_29_Haziran'
jwt = JWTManager(app)

# Endpoints

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    pw_hash = generate_password_hash(password)
    try: 
        db.insert_user(email, pw_hash)
    except psycopg2.IntegrityError:
        return jsonify({"error": "User already exists"}), 409

    return jsonify({"status": "ok"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    pw_hash = db.get_password_hash(email)
    if not pw_hash or not check_password_hash(pw_hash, password):
        return jsonify({"error": "Bad credentials"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"access_token": access_token}), 200

@app.route('/tasks/', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    email = request.args.get('email')
    if email != current_user:
        return jsonify({"error": "Unauthorized access"}), 403

    tasks = db.get_tasks(email)
    result = [
        {"id": t[0], "title": t[1], "is_completed": t[2]}
        for t in tasks
    ]
    return jsonify(result), 200

@app.route('/addTask/', methods=['POST'])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    email = request.args.get('email')
    if email != current_user:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({"error": "Title required"}), 400

    task_id = db.insert_task(email, title)
    return jsonify({"status": "ok", "task_id": task_id}), 201

@app.route('/deleteTask/', methods=['DELETE'])
@jwt_required()
def delete_task():
    current_user = get_jwt_identity()
    task_id = request.args.get('id')
    if not task_id:
        return jsonify({"error": "Task id required"}), 400

    owner = db.get_task_owner(int(task_id))
    if owner != current_user:
        return jsonify({"error": "Unauthorized or not found"}), 403

    db.delete_task(int(task_id))
    return jsonify({"status": "ok"}), 200

@app.route('/updateTask/', methods=['PATCH'])
@jwt_required()
def update_task():
    current_user = get_jwt_identity()
    task_id = request.args.get('id')
    is_completed = request.args.get('isCompleted')
    title = request.args.get('title')
    if not task_id or (is_completed is None and not title):
        return jsonify({"error": "id and isCompleted or title params required"}), 400

    is_completed_bool = is_completed.lower() == 'true'
    owner = db.get_task_owner(int(task_id))
    if owner != current_user:
        return jsonify({"error": "Unauthorized or not found"}), 403

    db.update_task(int(task_id), title, is_completed_bool)
    return jsonify({"status": "ok"}), 200

# Run
if __name__ == '__main__':
    app.run(debug=True)
