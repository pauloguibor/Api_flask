
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='The field "nome"can not be empty')
    argumentos.add_argument('estrelas', type=float, required=True, help='The field "estrelas" can not be empty')
    argumentos.add_argument('cidade')
    argumentos.add_argument('diaria')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'not found'}, 404
    
    @jwt_required()
    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {'message':f'hotel id {hotel_id} already exists'}, 400

        data = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except:
            return {'messagem': 'An unexpected erro ocurred trying to save hotel'}, 500
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):
        data = Hotel.argumentos.parse_args()

        hotel = HotelModel(hotel_id, **data)

        hotel_finded = HotelModel.find_hotel(hotel_id)

        if hotel_finded:
            hotel_finded.update_hotel(**data)
            hotel_finded.save_hotel()
            return hotel_finded.json(), 200

        hotel = HotelModel(hotel_id, **data)
        try:
            hotel.save_hotel()
        except:
            return {'messagem': 'An unexpected erro ocurred trying to save hotel'}, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'messagem': 'An unexpected erro ocurred trying to delete hotel'}, 500
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found'}, 404
