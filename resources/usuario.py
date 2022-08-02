from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be empty")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be empty")

class User(Resource):
    
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'not found'}, 404
    

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'messagem': 'An unexpected erro ocurred trying to delete User'}, 500
            return {'message': 'User deleted'}
        return {'message': 'User not found'}, 404

class UserRegister(Resource):

    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}
        
        dados['senha'] = generate_password_hash(dados['senha'], method='pbkdf2:sha256', salt_length=16)
        user = UserModel(**dados)
        user.save_user()
        
        return {'message': 'User created sucessfully!'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados["login"])

        if user and check_password_hash(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return{'access_token': token_de_acesso}, 200
        return {'message': 'username or password not correct'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] #jwt token
        BLACKLIST.add(jwt_id)
        return {'message': 'logged out successfully'}, 200
 
