from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy_serializer import SerializerMixin


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/new_flask'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# db.init_app(app)

# api = Api(app)

# @app.before_first_request
# def create_table():
#     db.create_all()

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'User'

#     id = db.Column(db.Integer, primary_key=True)
#     # Date_Created = db.Column(db.DateTime, default=datetime.utcnow)
#     # Last_Accessed = db.Column(db.DateTime, server_default=db.func.current_timestamp())
#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     cnic = db.Column(db.String(20))
#     date_of_birth = db.Column(db.DateTime)
#     province = db.Column(db.String(200))

#     def __init__(self, first_name, last_name, cnic,date_of_birth,province):
        
#         self.first_name = first_name 
#         self.last_name = last_name 
#         self.cnic = cnic 
#         self.date_of_birth = date_of_birth 
#         self.province = province 
    
#     def json(self):
#         return {"first_name":self.first_name,
#             "last_name":self.last_name,"cnic":self.cnic,"date_of_birth":self.date_of_birth,"province":self.province}



# parser = reqparse.RequestParser()

# class UserList(Resource):

#     def get(self):
#         result1 = User.query.all()
#         result =[x.to_dict() for x in result1]
#         return result

#     def post(self):
#         data = request.get_json()
#         dob= data["date_of_birth"]
#         date_of_birth1 = dob
#         new_user = User(data['first_name'],data['last_name'],data['cnic'],date_of_birth1,data['province'])
#         print(new_user)
#         db.session.add(new_user)
#         db.session.commit()
#         serialized = new_user.to_dict()
#         return serialized,201

# api.add_resource(UserList, '/user/')
# if __name__ == "__main__":
#   app.run(debug=True)