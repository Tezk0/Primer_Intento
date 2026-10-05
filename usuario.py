from mysqlconnection import connectToMySQL

DB_NAME = 'intento_certificacion'

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password_hash) VALUES (%(nombre)s, %(apellido)s,%(email)s, %(password_hash)s);"
        # %(dato)s = sentencia preparada
        return connectToMySQL(DB_NAME).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        resultados = connectToMySQL(DB_NAME).query_db(query)

        usuarios = []

        for usuario in resultados:
            usuarios.append(cls(usuario))

        return usuarios

    @classmethod
    def get_by_id(cls,datos):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultados = connectToMySQL(DB_NAME).query_db(query,datos)

        return cls(resultados[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s"
        resultado = connectToMySQL(DB_NAME).query_db(query, data)

        if len(resultado) < 1: #si es mas chico q 1 no retorna nada 
            return False
        return cls(resultado[0])

    @classmethod
    def borrar(cls, datos):
      query = "DELETE FROM usuarios WHERE id = %(id)s"

      resultado = connectToMySQL(DB_NAME).query_db(query, datos)

      if resultado is False:
         raise RuntimeError("Failed to delete user")

      return resultado

# Robado de mis anteriores tareas jijijiji