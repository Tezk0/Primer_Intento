from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from usuario import Usuario

app = Flask(__name__)

app.secret_key = "dhjfazhikgsdknlyrgyey5ejiogroir"

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/Registrar", methods=['POST'])
def registro():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email') 
    password = request.form.get('password')
    conf_password = request.form.get("conf_password")

    if password != conf_password:
        flash("Las contraseñas no coinciden.", "error")
        return redirect("/")

    if Usuario.get_by_email({"email": email}):
        flash("Ya existe una cuenta con ese correo.", "error")
        return redirect("/")
    
    try:
        user_id = Usuario.save({
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "password_hash": generate_password_hash(password)
        })

        if not user_id:
            flash("No se pudo crear la cuenta.", "error")
            return redirect("/")

    except ValueError as error:
        flash(str(error), "error")
        return redirect("/")

    session['user_id'] = user_id
    
    return redirect("/"), flash("Cuenta creada correctamente", "success")    

@app.route("/Login", methods=["POST"])
def login():

    data = {"email": request.form['email']}
    usuario_encontrado = Usuario.get_by_email(data)
    
    if not usuario_encontrado:
        flash("Usuario o contraseña incorrectos.", "login")
        return redirect("/")

    if check_password_hash(usuario_encontrado.password_hash, request.form['password']):
        session['user_id'] = usuario_encontrado.id
        print(f"Usuario numero {session['user_id']} ha iniciado sesiom")
        return redirect("/")
    
    flash("Usuario o contraseña incorrectos.", "login")
    return redirect("/")







if __name__ == "__main__":
    app.run(debug=True)