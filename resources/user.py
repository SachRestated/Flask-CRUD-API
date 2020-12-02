import sqlite3
from flask_restful import reqparse, Resource
from werkzeug.security import check_password_hash, generate_password_hash
from models.user_model import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required=True,
        help='This field cannot be blank'
    )
    parser.add_argument('password', 
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        data['password'] = generate_password_hash(data['password'])

        if UserModel.find_by_username(data['username']) is not None:
            return {'message': 'Account with this username already exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message' : 'User Created Successfully'}, 201
