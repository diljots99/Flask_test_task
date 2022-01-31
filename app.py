from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Blueprint
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.config["JWT_SECRET_KEY"] = "Authorization"  # Change this "super secret" with something else!
jwt = JWTManager(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Chat Room Api Implementation"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

socketio = SocketIO(app, manage_session=False)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

# Task 1 
class User(db.Model, SerializerMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    cnic = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime)
    province = db.Column(db.String(200))

    def __init__(self, first_name, last_name, cnic,date_of_birth,province):
        
        self.first_name = first_name 
        self.last_name = last_name 
        self.cnic = cnic 
        self.date_of_birth = date_of_birth 
        self.province = province 
    
    def json(self):
        return {"first_name":self.first_name,
            "last_name":self.last_name,"cnic":self.cnic,"date_of_birth":self.date_of_birth,"province":self.province}

# Task 2

class UserJWT(db.Model,SerializerMixin):
    __tablename__ = 'Userjwt'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, email, password):
        
        self.email = email 
        self.password = password 
         
    
    def json(self):
        return {"email":self.email,
            "password":self.password}


# Task 3
class User_game(db.Model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    Date_Created = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    Last_Accessed = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    # addresses = db.relationship('USER_GAME_RATING', backref='person', lazy=True)
    
    def __init__(self, first_name, last_name, Date_Created,Last_Accessed):
        self.Date_Created = Date_Created 
        self.Last_Accessed = Last_Accessed 
        self.first_name = first_name 
        self.last_name = last_name
        
    
    def json(self):
        return {"first_name":self.first_name,
            "last_name":self.last_name,"cnic":self.Date_Created,"date_of_birth":self.Last_Accessed}


class Game(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    Platform = db.Column(db.String(20))
    Avg_Rating = db.Column(db.String(20))
    # addresses = db.relationship('USER_GAME_RATING', backref='person', lazy=True)

    def __init__(self, name, Platform, Avg_Rating):
        
        self.name = name 
        self.Platform = Platform 
        self.Avg_Rating = Avg_Rating 
        
    
    def json(self):
        return {"name":self.name,
            "Platform":self.Platform,"Avg_Rating":self.Avg_Rating}


class USER_GAME_RATING(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user_game.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'),nullable=False)

    def __init__(self, Rating, user_id, game_id):
        
        self.Rating = Rating 
        self.user_id = user_id 
        self.game_id = game_id 
        
    
    def json(self):
        return {"Rating":self.Rating,
            "user_id":self.user_id,"game_id":self.game_id}

class UserGameView(Resource):
    # @swag_from("User Game", validation = True) 
    def get(self):
        result1 = User_game.query.all()
        result =[x.to_dict() for x in result1]
        return result
    # @swag_from("User Game", validation = True) 
    def post(self):
        data = request.get_json()
        # dob= data["date_of_birth"]
        # date_of_birth1 = dob
        new_user = User_game(data['first_name'],data['last_name'],data['Date_Created'],data['Last_Accessed'])
        
        db.session.add(new_user)
        db.session.commit()
        serialized = new_user.to_dict()
        return serialized,201

class GameView(Resource):

    def get(self):
        result1 = Game.query.all()
        result =[x.to_dict() for x in result1]
        return result

    def post(self):
        data = request.get_json()
        new_user = Game(data['name'],data['Platform'],data['Avg_Rating'])
        
        db.session.add(new_user)
        db.session.commit()
        serialized = new_user.to_dict()
        return serialized,201

class UserGameRatingView(Resource):

    def get(self):
        result1 = USER_GAME_RATING.query.all()
        result =[x.to_dict() for x in result1]
        return result

    def post(self):
        data = request.get_json()
        new_user = USER_GAME_RATING(data['Rating'],data['user_id'],data['game_id'])
        
        db.session.add(new_user)
        db.session.commit()
        serialized = new_user.to_dict()
        return serialized,201



# Task 4
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))

@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)

parser = reqparse.RequestParser()

class UserList(Resource):

    def get(self):
        result1 = User.query.all()
        result =[x.to_dict() for x in result1]
        return result

    def post(self):
        data = request.get_json()
        dob= data["date_of_birth"]
        date_of_birth1 = dob
        new_user = User(data['first_name'],data['last_name'],data['cnic'],date_of_birth1,data['province'])
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        serialized = new_user.to_dict()
        return serialized,201


class UserRegistration(Resource):
    @jwt_required()
    def get(self):
        result1 = UserJWT.query.all()
        result =[x.to_dict() for x in result1]
        return result

    def post(self):
        data = request.get_json()
        new_user = UserJWT(data['email'],data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        serialized = new_user.to_dict()
        return serialized,201


# class JWTTokenGenerator(Resource):
@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = UserJWT.query.filter_by(email=email, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })


api.add_resource(UserList, '/user/')
api.add_resource(UserGameView, '/userview/')
api.add_resource(GameView, '/usergame/')
api.add_resource(UserGameRatingView, '/rating/')
api.add_resource(UserRegistration, '/registration/')
# api.add_resource(JWTTokenGenerator, '/token/')


if __name__ == '__main__':
    socketio.run(app)
    # app.run(debug=True)

# if __name__ == "__main__":
#   app.run(debug=True)


# Url for task
# 1 Validation  for user is /user/
# 2 jwt  auth for resistration /registration/ and generation /token/ and varify /registration/ get method
# query set foe user /userview/ and game /usergame/ and rating /rating/
# for chat room /index 