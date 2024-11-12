from flask import Flask, app, request, jsonify
app = Flask(__name__)
import mysql.connector
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='todo_app'
    )
    
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    todo_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({'id': todo_id, 'title': title, 'description': description, 'completed': False}), 201


@app.route('/todos', methods=['GET'])  #Get all todos
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(todos)

@app.route('/todos/<int:id>', methods=['GET'])   #get sinlge todo
def get_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos WHERE id = %s", (id,))
    todo = cursor.fetchone()
    cursor.close()
    conn.close()

    if todo:
        return jsonify(todo)
    else:
        return jsonify({'error': 'To-do item not found'}), 404
    
    
    
@app.route('/todos/<int:id>', methods=['PUT'])   #update todo
def update_todo(id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET title = %s, description = %s, completed = %s WHERE id = %s",
        (title, description, completed, id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'To-do item updated successfully'})


@app.route('/todos/<int:id>', methods=['DELETE']) #delet todo
def delete_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'To-do item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)