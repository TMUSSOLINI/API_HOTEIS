from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id':'alpha',
        'nome': 'Alpha hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id':'bravo',
        'nome': 'Bravo hotel',
        'estrelas': 4.4,
        'diaria': 380.34,
        'cidade': 'Santa catarina'
    },
    {
        'hotel_id':'charlie',
        'nome': 'Charlie hotel',
        'estrelas': 3.9,
        'diaria': 390.34,
        'cidade': 'Santa catarina'
    }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumento = reqparse.RequestParser()
    argumento.add_argument('nome')
    argumento.add_argument('estrelas')
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')


    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None


    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel não encontrado.'}, 404


    def post(self, hotel_id):
        dados = Hotel.argumento.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 200


    def put(self, hotel_id):
        dados = Hotel.argumento.parse_args()
        hotel = Hotel.find_hotel(hotel_id)
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200
        hoteis.append(novo_hotel)
        return novo_hotel, 201


    def delete(self, hotel_id):
        global hoteis
        hoteis = [ hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deletado.'}
