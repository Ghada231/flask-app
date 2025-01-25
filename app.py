from flask import Flask, jsonify, request  
# Importer Flask pour créer l'application

from flask_sqlalchemy import SQLAlchemy  
# Importer SQLAlchemy pour gérer la BD

from flask_migrate import Migrate  
# Importer Flask-Migrate pour faciliter les migrations de la BD

app = Flask(__name__)  
# Initialiser une application Flask

db = SQLAlchemy()  
# Créer une instance de SQLAlchemy 

db.init_app(app)  
# Associer l'instance SQLAlchemy à l'application Flask.


# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgre:postgre@db:5432/db'  




# Définition du modèle Task 
class Task(db.Model):  
    __tablename__ = 'tasks'  # Nom explicite de la table dans la base.
    id = db.Column(db.Integer, primary_key=True)  
    # id : clé primaire
    title = db.Column(db.String(80), nullable=False)  
    # title : stocke un texte 

    def dictionnaire(self):  
        #convertir un objet Task en dictionnaire 
        return {'id': self.id, 'title': self.title}

migrate = Migrate(app, db)  
# Lier Flask-Migrate à l'application et BD

@app.route('/')  
# route de base ('/')
def text():  
    return 'HELLO TO MY FLASK APP!'  
    # tester le fontionnement de l'application

@app.route('/GetTasks', methods=['GET'])  
# Route pour obtenir les tâches avec GET
def get():  
    tasks = Task.query.all()  
    return jsonify([task.dictionnaire() for task in tasks])  

@app.route('/AddTasks', methods=['POST'])  
# Route pour ajouter une nouvelle tâche avec POST
def add():  
    data = request.get_json()  
    if not data or 'title' not in data:  
        return jsonify({'error': 'Invalid request'}), 400  
    task = Task(title=data['title'])  
    # Créer une nouvelle tâche avec le titre donné
    db.session.add(task)   
    db.session.commit()  
    return jsonify(task.dictionnaire()), 201  

@app.route('/UpdateTasks/<int:id>', methods=['PUT'])  
# Route pour MAJ une tâche par id 
def update(id):  
    task = Task.query.get(id)  
    if not task:  
        # Vérifier si la tâche existe
        return jsonify({'error': 'Task not found'}), 404  
    data = request.get_json()  
    task.title = data.get('title', task.title)  
    db.session.commit()  
    return jsonify(task.dictionnaire())  

@app.route('/DeleteTasks/<int:id>', methods=['DELETE'])  
# Route pour supprimer une tâche par id 
def delete(id):  
    task = Task.query.get(id)  
    if not task:  
        # Vérifier si la tâche existe
        return jsonify({'error': 'Task not found'}), 404  
    db.session.delete(task)  
    db.session.commit()  
    return jsonify({'message': 'Task deleted'})  

@app.errorhandler(404)  
def handle_404(error):  
    return jsonify({'error': 'Route not found'}), 404  
    # Retourner une erreur 404 au format JSON pour les routes inconnues

if __name__ == '__main__':   
    app.run(debug=True)  
