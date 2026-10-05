from mysqlconnection import connectToMySQL

DB_NAME = 'intento_certificacion'

class Pelicula:
    def __init__(self, data):
        self.nombre_pelicula = data['nombre_pelicula']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod