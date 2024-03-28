

import os
from flask import Flask, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(15), unique=True, nullable=False)
    age = db.Column(db.Integer)
    image = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Retrieve all users from the database
    user_list = []  # Initialize an empty list to store user data as dictionaries

    # Loop through the users and create a dictionary representation for each user
    for user in users:
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'age': user.age,
            'image': user.image,
            'created_at': user.created_at.isoformat(),  # Convert to ISO format for JSON serialization
            'bio': user.bio
            # Add other attributes as needed
        }
        user_list.append(user_data)  # Append the user data to the list

    return jsonify(user_list)  # Return the list of users as JSON

@app.route('/api/users', methods=['POST'])
def create_users():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    age = data.get('age')
    image = data.get('image')
    bio = data.get('bio')

    new_user = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        age=age,
        image=image,
        bio=bio
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
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        age = data.get('age')
        image = data.get('image')
        bio = data.get('bio')

        # Update the user's attributes
        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.age = age
        user.image = image
        user.bio = bio

        # Commit changes to the database
        db.session.commit()

        # Return a response indicating successful update (optional)
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
        }), 200  # Return status code 200 for success

    # If the request method is GET, you may return the user details or perform other actions

    return jsonify({
        'message': 'This endpoint supports POST method for editing user details.'
    }), 405  # Return status code 405 for Method Not Allowed

if __name__ == '__main__':
    app.run(debug=True)






