from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2003',
    'database': 'svd_test'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Sample query to fetch data
        cursor.execute('SELECT * FROM users')
        results = cursor.fetchall()
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Get JSON data from request
        data = request.json
        username = data['username']
        password = data['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert user data into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        
        return jsonify({'message': 'User added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete user by username
        cursor.execute('DELETE FROM users WHERE username = %s', (username,))
        conn.commit()
        
        # Check if any rows were affected
        if cursor.rowcount == 0:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
