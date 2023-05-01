from flask_restful import Resource, reqparse
from models.hotel import HotelModel


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    argumento = reqparse.RequestParser()
    argumento.add_argument('nome', type=str, required=True, help="O campo 'nome', não pode estar vazio!")
    argumento.add_argument('estrelas', type=float, required=True, help="O campo 'estrelas', não pode estar vazio!")
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado.'}, 404


    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id: '{}', ja existe!".format(hotel_id)}, 400

        dados = Hotel.argumento.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Houve um erro interno, na hora de salvar os dados!'}, 500
        return hotel.json()
        


    def put(self, hotel_id):
        dados = Hotel.argumento.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Houve um erro interno, na hora de salvar os dados!'}, 500
        return hotel.json(), 201


    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Ocorreu um erro ao tentar deletar!'}, 500
            return {"message": "Hotel {} deletado.".format(hotel_id)}
        return {'message': 'Hotel não encontrado.'}, 404

