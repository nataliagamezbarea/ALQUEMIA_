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
        cliente_tipo = request.form.get("cliente_tipo", "False")  # False por defecto (particular)

        # Validación de coincidencia de contraseñas
        if contrasena != confirmar_contrasena:
            return render_template(
                "authentication/registro.html",
                error="Las contraseñas no coinciden.",
                cliente_tipo=cliente_tipo
            )

        # Si es empresa, el correo debe terminar en @tiendalquemia.com
        if cliente_tipo == "True" and not email.endswith("@tiendalquemia.com"):
            return render_template(
                "authentication/registro.html",
                error="Para cuentas de empresa, el correo debe terminar en @tiendalquemia.com.",
                cliente_tipo=cliente_tipo
            )

        # Accedemos a la tabla 'usuarios'
        Usuario = obtener_tabla('usuarios')
        session_db = Session(db.engine)

        # Verificamos si ya existe un usuario con ese correo
        if session_db.query(Usuario).filter_by(email=email).first():
            session_db.close()
            return render_template(
                "authentication/registro.html",
                error="Correo electrónico ya registrado.",
                cliente_tipo=cliente_tipo
            )

        # Se determina si el usuario será administrador
        is_admin = cliente_tipo == "True"

        # Encriptamos la contraseña para guardarla de forma segura
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

        # Se crea un nuevo usuario con los datos del formulario
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido1=apellido1,
            apellido2=apellido2,
            email=email,
            contrasena=contrasena_encriptada.decode("utf-8"),
            is_admin=is_admin
        )

        # Guardamos el usuario en la base de datos
        session_db.add(nuevo_usuario)
        session_db.commit()
        session_db.close()

        # Redirigimos al login tras el registro exitoso
        return redirect(url_for("login"))

    # Si es una petición GET, mostramos el formulario vacío
    return render_template("authentication/registro.html", cliente_tipo=None)
