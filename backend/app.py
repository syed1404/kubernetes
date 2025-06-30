from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'NewPass123',
    'database': 'user_data'
}
def get_db_connection():
    return psycopg2.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            dbname=db_config['database'],
            cursor_factory=RealDictCursor)

@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    name, email, age = data['name'], data['email'], data['age']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/api/get_users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
