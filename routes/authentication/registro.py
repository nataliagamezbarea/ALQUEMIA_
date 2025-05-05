# routes/authentication/registro.py

from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import Session
from backend.base_de_datos import obtener_tabla, db  # Importamos funciones y la base de datos
import bcrypt

def registro():
    if request.method == "POST":
        # Tomamos los datos que el usuario escribió en el formulario
        nombre = request.form["nombre"]
        apellido1 = request.form.get("apellido1", "")
        apellido2 = request.form.get("apellido2", "")
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        confirmar_contrasena = request.form["confirmar_contrasena"]

        # Si las contraseñas no coinciden, se muestra un error
        if contrasena != confirmar_contrasena:
            return render_template(
                "authentication/registro.html",
                error="Las contraseñas no coinciden.",
                cliente_tipo=request.form.get('cliente_tipo')
            )

        # Accedemos a la tabla 'usuarios' de la base de datos
        Usuario = obtener_tabla('usuarios')

        # Creamos una sesión para interactuar con la base de datos
        session_db = Session(db.engine)

        # Verificamos si ya hay un usuario con ese correo
        usuario_existente = session_db.query(Usuario).filter_by(email=email).first()
        if usuario_existente:
            session_db.close()
            return render_template(
                "authentication/registro.html",
                error="Correo electrónico ya registrado.",
                cliente_tipo=request.form.get('cliente_tipo')
            )

        # Revisamos si se registró como administrador
        cliente_tipo = request.form.get("cliente_tipo", "False")
        is_admin = True if cliente_tipo == "True" else False

        # Encriptamos la contraseña para guardarla de forma segura
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

        # Creamos un nuevo usuario con los datos recibidos
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            email=email,
            contrasena=contrasena_encriptada.decode("utf-8"),
            is_admin=is_admin
        )

        # Guardamos al nuevo usuario en la base de datos
        session_db.add(nuevo_usuario)
        session_db.commit()
        session_db.close()

        # Redirigimos al login después del registro exitoso
        return redirect(url_for("login"))

    # Si es una petición GET, mostramos el formulario
    return render_template("authentication/registro.html", cliente_tipo=None)
