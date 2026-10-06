from flask_app import app

from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash


from flask_app.models.usuario import Usuario
from flask_app.models.comentario import Comentario
from flask_app.models.pelicula import Pelicula

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
        session['nombre'] = usuario_encontrado.nombre
        session['apellido'] = usuario_encontrado.apellido

        print(f"Usuario numero {session['user_id']} ha iniciado sesiom")
        return redirect("/cine")
    
    flash("Usuario o contraseña incorrectos.", "login")
    return redirect("/")

@app.route("/cine")
def peliculas():
    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")

    usuario_id = {
        'id': session['user_id']
    }

    usuario_sesion = Usuario.get_by_id(usuario_id)

    print(f"id de usuario {session['user_id']}")

    peliculas = Pelicula.get_all()

    return render_template("peliculas.html", usuario_sesion=usuario_sesion, peliculas=peliculas)

@app.route("/nuevo")
def form_peli():

    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")

    usuario_id = {
        'id': session['user_id']
    }

    usuario_sesion = Usuario.get_by_id(usuario_id)

    return render_template("form_peli.html", usuario_sesion=usuario_sesion)

@app.route("/Crear_peli", methods=['POST'])
def crear_peli():

    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")
    
    nombre_pelicula = request.form.get("nombre_pelicula")
    director = request.form.get("director")
    fecha_estreno = request.form.get("fecha_estreno")
    sinopsis = request.form.get("sinopsis")
    usuario_id = request.form.get("usuario_id")

    if Pelicula.check_duplicates({"nombre_pelicula": nombre_pelicula}):
        flash("Ya existe una pelicula con ese nombre", "error")
        return redirect("/nuevo")
    
    if sinopsis == '':
        flash("Sinopsis no puede estar vacía", "error")
        return redirect("/nuevo")

    try:
        pelicula_id = Pelicula.save({
            "nombre_pelicula": nombre_pelicula,
            "director": director,
            "fecha_estreno": fecha_estreno,
            "sinopsis": sinopsis,
            "usuario_id": usuario_id
        })

        if not pelicula_id:
            flash("No se pudo crear la pelicula", "error")
            return redirect("/nuevo")

    except ValueError as error:
        flash(str(error), "error")
        return redirect("/nuevo")

    
    return redirect(f"/cine/{pelicula_id}")

@app.route("/cine/<int:pelicula_id>")
def mostrar_pelicula(pelicula_id):

    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")

    data = {
        "id": pelicula_id
    }
    pelicula = Pelicula.get_by_id(data)

    data_usuario = {
        "id": pelicula.usuario_id
    }

    usuario_pelicula = Usuario.get_by_id(data_usuario)

    comentarios = Comentario.get_all_by_user_id({
        "peliculas_id": pelicula_id
    })

    usuario = Usuario.get_by_id({
        "id": session['user_id']
    })

    return render_template("pelicula.html", pelicula=pelicula, usuario_pelicula=usuario_pelicula, comentarios=comentarios, usuario=usuario)

@app.route("/editar/<int:pelicula_id>")
def editar(pelicula_id):

    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")

    data = {
        "id": pelicula_id
    }

    pelicula = Pelicula.get_by_id(data)

    data_usuario = {
        "id": pelicula.usuario_id
    }

    usuario_autor = Usuario.get_by_id(data_usuario)

    if usuario_autor.id != session['user_id']:
        flash("No eres autor de esta pelicula!", "error")
        return redirect("/cine")

    return render_template("form_editar.html", pelicula=pelicula, usuario_autor=usuario_autor)

@app.route("/Editar_peli", methods=['POST'])
def editarpeli():
    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")

    id_pelicula = request.form.get("id_pelicula")
    nombre_pelicula = request.form.get("nombre_pelicula")
    director = request.form.get("director")
    fecha_estreno = request.form.get("fecha_estreno")
    sinopsis = request.form.get("sinopsis")

    if nombre_pelicula == '':
        flash("Nombre no puede estar vacio", "error")
        return redirect(f"/editar/{id_pelicula}")

    if director == '':
        flash("Una pelicula no puede existir sin director", "error")
        return redirect(f"/editar/{id_pelicula}")

    if fecha_estreno == '':
        flash("Fecha de Estreno no puede estar vacio", "error")
        return redirect(f"/editar/{id_pelicula}")

    if sinopsis == '':
        flash("Sinopsis no puede estar vacio", "error")
        return redirect(f"/editar/{id_pelicula}")

    Pelicula.update({
        "id": id_pelicula,
        "nombre_pelicula": nombre_pelicula,
        "director": director,
        "fecha_estreno": fecha_estreno,
        "sinopsis": sinopsis
    })

    return redirect(f"/cine/{id_pelicula}")
    
@app.route("/borrar/<int:pelicula_id>")
def borrar(pelicula_id):

    if 'user_id' not in session:
        flash("Inicia sesion antes de ingresar, pillo", "error")
        return redirect("/")

    data_para_obtener_usuario = {
        "id": pelicula_id
    }

    pelicula = Pelicula.get_by_id(data_para_obtener_usuario)

    data_usuario = {
        "id": pelicula.usuario_id
    }

    usuario_autor = Usuario.get_by_id(data_usuario)

    data = {
        "id": pelicula_id
    }

    if usuario_autor.id != session['user_id']:
        flash("No eres autor de esta pelicula!", "error")
        return redirect("/cine")

    Pelicula.delete(data)

    return redirect("/cine")

@app.route("/comentar", methods=['POST'])
def comentar():
    usuario_id = request.form.get("usuario_id")
    pelicula_id = request.form.get("pelicula_id")
    comentario = request.form.get("comentario")

    Comentario.save({
        "usuarios_id": usuario_id,
        "peliculas_id": pelicula_id,
        "comentario": comentario
    })

    return redirect(f"/cine/{pelicula_id}")


@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/")