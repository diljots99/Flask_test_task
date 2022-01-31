from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/new_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    Date_Created = db.Column(db.DateTime, default=datetime.utcnow)
    Last_Accessed = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    cnic = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime)
    province = db.Column(db.String(200))

    def __init__(self,Date_Created,Last_Accessed, first_name, last_name, cnic,date_of_birth,province):
        self.Date_Created = Date_Created
        self.Last_Accessed = Last_Accessed
        self.first_name = first_name 
        self.last_name = last_name 
        self.cnic = cnic 
        self.date_of_birth = date_of_birth 
        self.province = province 
    
    def json(self):
        return {"Date_Created":self.Date_Created, "Last_Accessed":self.Last_Accessed, "first_name":self.first_name,
            "last_name":self.last_name,"cnic":self.cnic,"date_of_birth":self.date_of_birth,"province":self.province}


parser = reqparse.RequestParser()

class UserList(Resource):

    def get(self):
        result1 = User.query.all()
        # print(result)
        for result in result1:

            data = {
                "id":result.id,
                "Date_Created":result.Date_Created,
                "Last_Accessed":result.Last_Accessed,
                "first_name":result.first_name,
                "last_name":result.last_name,
                "cnic":result.cnic,
                "date_of_birth":result.date_of_birth,
                "province":result.province
            }
        user_data = jsonify(data)
        # data = jsonify(result)
        return user_data
        # return {'Books':list(x.dumps() for x in result)}
        # return {'Books':list(jsonify(x) for x in result)}

    
    def post(self):
        data = request.get_json()
        new_user = User(data['Date_Created'],data['Last_Accessed'],data['first_name'],data['last_name'],data['cnic'],data['date_of_birth'],data['province'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.json(),201

api.add_resource(UserList, '/user/')

if __name__ == "__main__":
  app.run(debug=True)