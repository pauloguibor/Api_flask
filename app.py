from flask import Flask
from flask_restful import Resource, Api
from resources.hotel import Hoteis, Hotel

app = Flask(__name__)
api = Api(app)

class Teste(Resource):
    def get(self):
        return {'hoteis': 'dale get'}

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')
api.add_resource(Teste, '/')

if __name__ == '__main__':
    app.run(debug=True)