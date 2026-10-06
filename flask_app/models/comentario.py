from flask_app.config.mysqlconnection import connectToMySQL
DB_NAME = 'intento_certificacion'

class Comentario:
    def __init__(self, data):
        self.usuario_id = data['usuarios_id']
        self.pelicula_id = data['peliculas_id']
        self.comentario = data['comentario']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comentarios;"
        resultados = connectToMySQL(DB_NAME).query_db(query)

        comentarios = []

        for comentario in resultados:
            comentarios.append(cls(comentario))

        return comentarios

    @classmethod
    def get_all_by_user_id(cls, data):
        query = "SELECT * FROM comentarios WHERE peliculas_id = %(peliculas_id)s;"
        resultados = connectToMySQL(DB_NAME).query_db(query, data)

        comentarios = []

        for comentario in resultados:
            comentarios.append(cls(comentario))

        return comentarios

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comentarios (usuarios_id, peliculas_id, comentario) VALUES (%(usuarios_id)s, %(peliculas_id)s,%(comentario)s);"
        # %(dato)s = sentencia preparada
        return connectToMySQL(DB_NAME).query_db(query, data)

    @classmethod
    def get_user_info(cls, data):
        query = "SELECT usuarios_id FROM comentarios WHERE peliculas_id = %(peliculas_id)s"
        resultados = connectToMySQL(DB_NAME).query_db(query, data)

        if len(resultados) < 1: #si es mas chico q 1 no retorna nada 
            return False    
        return cls(resultados[0])

    