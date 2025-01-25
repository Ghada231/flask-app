from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgre:postgre@db:5432/db'  # Database URI (Required)

db.init_app(app)

class Task(db.Model):
    __tablename__ = 'tasks'  # Explicitly set the table name
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    title = db.Column(db.String(80), nullable=False)  # Task title (required)

    def dictionnaire(self):
        return {'id': self.id, 'title': self.title}

migrate = Migrate(app, db)  # Bind Flask-Migrate to the app and database (Required)

@app.route('/')
def text():
    return 'FLASK REST API YEY'

@app.route('/GetTasks', methods=['GET'])
def get():
    tasks = Task.query.all()  # Fetch all tasks from the database
    return jsonify({"awatef":"awatef"})  # Return tasks in JSON format

@app.route('/AddTasks', methods=['POST'])
def add():
    data = request.get_json()  # Parse JSON request body
    if not data or 'title' not in data:  # Validate required fields
        return jsonify({'error': 'Invalid request'}), 400
    task = Task(title=data['title'])  # Create new task
    db.session.add(task)  # Add to session
    db.session.commit()  # Commit changes to the database
    return jsonify(task.dictionnaire()), 201  # Return created task in JSON format

@app.route('/UpdateTasks/<int:id>', methods=['PUT'])
def update(id):
    task = Task.query.get(id)  # Fetch task by ID
    if not task:  # Check if task exists
        return jsonify({'error': 'Task not found'}), 404
    data = request.get_json()  # Parse JSON request body
    task.title = data.get('title', task.title)  # Update title if provided
    db.session.commit()  # Commit changes
    return jsonify(task.dictionnaire())  # Return updated task in JSON format

@app.route('/DeleteTasks/<int:id>', methods=['DELETE'])
def delete(id):
    task = Task.query.get(id)  # Fetch task by ID
    if not task:  # Check if task exists
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)  # Mark task for deletion
    db.session.commit()  # Commit deletion
    return jsonify({'message': 'Task deleted'})  # Return success message in JSON format

@app.errorhandler(404)
def handle_404(error):
    return jsonify({'error': 'Route not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(debug=True)
