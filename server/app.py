from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
from flask_cors import CORS


CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():

    messages = Message.query.all()

    messages_dict = [message.to_dict() for message in messages]

    response = make_response(
        messages_dict,
        200,
        {"Content-Type": "application/json"}

    )
    return response

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if message:
        message_dict = message.to_dict()

        response = make_response(
        message_dict,
        200,
        )
        return response

    return jsonify({"error": "id not found"})

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    new_msg = Message(
        body=data.get('body'),
        username=data.get('username')
    )

    db.session.add(new_msg)
    db.session.commit()

    return jsonify(new_msg.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = Message.query.get(id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()
    msg.body = data.get('body', msg.body)
    db.session.commit()

    return jsonify(msg.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.get(id)

    if not msg:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(msg)
    db.session.commit()
    return jsonify({}), 204


if __name__ == '__main__':
    app.run(port=5555)
