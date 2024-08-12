import os
from flask import Flask, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.exceptions import BadRequest

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer)
    image = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'age': user.age,
        'image': user.image,
        'created_at': user.created_at.isoformat(),
        'bio': user.bio
    } for user in users]

    return jsonify(user_list)


@app.route('/api/users', methods=['POST'])
def create_users():
    data = request.get_json()
    if not data:
        raise BadRequest('Invalid JSON data')

    required_fields = ['firstname', 'lastname', 'email']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f'Missing required field: {field}')

    new_user = User(
        firstname=data['firstname'],
        lastname=data['lastname'],
        email=data['email'],
        age=data.get('age'),
        image=data.get('image'),
        bio=data.get('bio')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'firstname': new_user.firstname,
        'lastname': new_user.lastname,
        'email': new_user.email,
        'age': new_user.age,
        'image': new_user.image,
        'created_at': new_user.created_at.isoformat(),
        'bio': new_user.bio
    }), 201


@app.route('/api/users/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            raise BadRequest('Invalid JSON data')

        user.firstname = data.get('firstname', user.firstname)
        user.lastname = data.get('lastname', user.lastname)
        user.email = data.get('email', user.email)
        user.age = data.get('age', user.age)
        user.image = data.get('image', user.image)
        user.bio = data.get('bio', user.bio)

        db.session.commit()

        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'age': user.age,
                'image': user.image,
                'created_at': user.created_at.isoformat(),
                'bio': user.bio
            }
        }), 200

    return jsonify({
        'message': 'This endpoint supports POST method for editing user details.'
    }), 405


if __name__ == '__main__':
    app.run(debug=True)
