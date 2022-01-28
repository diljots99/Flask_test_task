from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
User = {
    '1': {'first_name': 'Mark', 'last_name': 'This', 'spec': 'math'},
    '2': {'name': 'Jane', 'last_name': 'This', 'spec': 'biology'},
    '3': {'name': 'Peter', 'last_name': 'This', 'spec': 'history'},
    '4': {'name': 'Kate', 'last_name': 'This', 'spec': 'science'},
}

parser = reqparse.RequestParser()

class UserList(Resource):

    def get(self):
        return User

    
    def post(self):
        parser.add_argument("first_name")
        parser.add_argument("last_name")
        parser.add_argument("cnic")
        parser.add_argument("date_of_birth")
        parser.add_argument("province")
        args = parser.parse_args()
        user_id = int(max(User.keys())) + 1
        user_id = '%i' % user_id
        User[user_id] = {
            "first_name": args["first_name"],
            "last_name": args["last_name"],
            "cnic": args["cnic"],
            "date_of_birth": args["date_of_birth"],
            "province": args["province"]
        }
        return User[user_id], 201

api.add_resource(UserList, '/user/')

if __name__ == "__main__":
  app.run(debug=True)