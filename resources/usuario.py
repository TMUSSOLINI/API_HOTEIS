from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuario não encontrado.'}, 404


    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'Ocorreu um erro ao tentar deletar!'}, 500
            return {"message": "Usuario {} deletado.".format(user_id)}
        return {'message': 'Usuario não encontrado.'}, 404


class UserRegister(Resource):
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="O campo 'Login', não pode ser vazio!")
        atributos.add_argument('senha', type=str, required=True, help="O campo 'senha', não pode ficar vazio!")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': "O usuario '{}', ja existe!".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Usuario criado com sucesso!'}, 201
