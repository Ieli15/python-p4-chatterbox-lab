from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET all messages (ordered by created_at)
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200

# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data.get('body'),
        username=data.get('username'),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
        message.updated_at = datetime.utcnow()
        db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return {}, 204

if __name__ == '__main__':
    app.run(port=5555)
