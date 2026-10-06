from flask import Flask #Importación de Flask

app = Flask(__name__) #Crea instancia de Flask

app.secret_key = "fsdagfdjfasjfsajfajkfa" #Clave secreta para sesiones y seguridad

#Ta copiao del proyeto tacos