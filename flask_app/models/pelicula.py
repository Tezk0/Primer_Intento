from flask_app.config.mysqlconnection import connectToMySQL

DB_NAME = 'intento_certificacion'

class Pelicula:
    def __init__(self, data):
        self.id = data['id']
        self.nombre_pelicula = data['nombre_pelicula']
        self.director = data['director']
        self.fecha_estreno = data['fecha_estreno']
        self.sinopsis = data['sinopsis']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM peliculas;"
        resultados = connectToMySQL(DB_NAME).query_db(query)

        peliculas = []

        for pelicula in resultados:
            peliculas.append(cls(pelicula))

        return peliculas

    @classmethod
    def save(cls, data):
        query = "INSERT INTO peliculas (nombre_pelicula, director, fecha_estreno, sinopsis, usuario_id) VALUES(%(nombre_pelicula)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s)"
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def check_duplicates(cls, data):
        query = "SELECT * FROM peliculas WHERE nombre_pelicula = %(nombre_pelicula)s"
        resultado = connectToMySQL(DB_NAME).query_db(query, data)

        if len(resultado) < 1: #si es mas chico q 1 no retorna nada 
            return False    
        return cls(resultado[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM peliculas WHERE id = %(id)s;"
        resultados = connectToMySQL(DB_NAME).query_db(query,data)

        return cls(resultados[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE peliculas
            SET nombre_pelicula = %(nombre_pelicula)s,
            director = %(director)s,
            fecha_estreno = %(fecha_estreno)s,
            sinopsis = %(sinopsis)s
            WHERE id = %(id)s;
        """
        resultado = connectToMySQL(DB_NAME).query_db(query, data)

        return resultado  

    @classmethod 
    def delete(cls, data):
        query = "DELETE FROM peliculas WHERE id = %(id)s"

        resultado = connectToMySQL(DB_NAME).query_db(query, data)

        if resultado is False:
            raise RuntimeError("Fallo eliminar la pelicula")

        return resultado
