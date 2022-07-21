from click import argument
from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id':'alpha',
        'nome':'Alpha hotel',
        'estrelas':'4.3',
        'diaria':'420.0',
        'cidade': 'rio de janeiro'
    },
    {
        'hotel_id':'bravo',
        'nome':'bravo hotel',
        'estrelas':'4.3',
        'diaria':'420.0',
        'cidade': 'florianopolis'
    },
    {
        'hotel_id':'charlie',
        'nome':'charlie hotel',
        'estrelas':'4.3',
        'diaria':'420.0',
        'cidade': 'florianopolis'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('cidade')
    argumentos.add_argument('diaria')

    def findhotel(hotel_id):
        for hotel in hoteis:
            if(hotel['hotel_id'] == hotel_id):
                return hotel
        return None

    
    def get(self, hotel_id):
        hotel = Hotel.findhotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'not found'}, 404
    
    
    def post(self, hotel_id):

        data = Hotel.argumentos.parse_args()

        hotel_obj = HotelModel(hotel_id, **data)

        novo_hotel = hotel_obj.json()
        #novo_hotel = {'hotel_id': hotel_id, **data } #modelo antigo

        hoteis.append(novo_hotel)
        return hoteis, 200

    def put(self, hotel_id):
        data = Hotel.argumentos.parse_args()

        hotel_obj = HotelModel(hotel_id, **data)

        novo_hotel = hotel_obj.json()

        hotel = Hotel.findhotel(hotel_id)

        if hotel:
            hotel.update(novo_hotel)
            return hoteis, 200

        hoteis.append(novo_hotel)
        return hoteis, 201



    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message' : 'hotel deleted.'}

