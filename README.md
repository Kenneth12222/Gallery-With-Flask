user1 = User(
    firstname='Karolina', 
    lastname='Grabowska', 
    email='Karolina12@gmail.com', 
    age= 35,
    image='https://images.pexels.com/photos/6919954/pexels-photo-6919954.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='Content Creator'
)



user2 = User(
    firstname='George', 
    lastname='Milton', 
    email='Milton12@gmail.com', 
    age= 28,
    image='https://images.pexels.com/photos/6953881/pexels-photo-6953881.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='Middleware Developer'
)



user3 = User(
    firstname='Blue', 
    lastname='Bird', 
    email='bird12@gmail.com', 
    age= 25,
    image='https://images.pexels.com/photos/7242768/pexels-photo-7242768.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='Data Scientist'
)


user4 = User(
    firstname='Andres', 
    lastname='Ayrton', 
    email='Andresayrton12@gmail.com', 
    age= 29,
    image='https://images.pexels.com/photos/6579062/pexels-photo-6579062.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='BackEnd Game Developer'
)



user5 = User(
    firstname='Zen', 
    lastname='Chung', 
    email='Zchug12@gmail.com', 
    age= 25,
    image='https://images.pexels.com/photos/5538320/pexels-photo-5538320.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='DevOps'
)


user6 = User(
    firstname='Ono', 
    lastname='Kosuki', 
    email='Onokosuki12@gmail.com', 
    age= 75,
    image='https://images.pexels.com/photos/5647214/pexels-photo-5647214.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='Database Developer'
)


user7 = User(
    firstname='Friday', 
    lastname='Danzor', 
    email='Danzor12@gmail.com', 
    age= 38,
    image='https://images.pexels.com/photos/4600301/pexels-photo-4600301.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
    bio='Json Developer'
)






























import os
from flask import Flask, jsonify, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(15), unique=True, nullable=False)
    age = db.Column(db.Integer)
    image = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'age': user.age,
            'image': user.image,
            'created_at': user.created_at.isoformat(),
            'bio': user.bio
        }
        user_list.append(user_data)

    return jsonify(user_list)

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

if __name__ == '__main__':
    app.run(debug=True)
