from flask import redirect, render_template, request, session
import bcrypt
from sqlalchemy.orm import Session
from backend.base_de_datos import db, obtener_tabla  # Se importa obtener_tabla para acceder al modelo reflejado

def login():
    Usuario = obtener_tabla("usuarios")  # Modelo reflejado directamente aquí

    # Si ya hay sesión activa, redirige según tipo de usuario
    if "user" in session:
        if session.get("is_admin"):
            return render_template("admin/admin.html")
        # return redirect(url_for('informacion_personal'))

    if request.method == "POST":
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")

        session_db = Session(db.engine)  # Conexión a la base de datos

        usuario = session_db.query(Usuario).filter_by(email=email).first()

        if usuario and bcrypt.checkpw(contrasena.encode("utf-8"), usuario.contrasena.encode("utf-8")):
            session["user"] = usuario.id_usuario
            session["is_admin"] = getattr(usuario, "is_admin", False)
            session_db.close()

            if session["is_admin"]:
                return render_template("admin/admin.html")
            # return redirect(url_for("informacion_personal"))
        else:
            session_db.close()
            return render_template("authentication/login.html", error="Email o contraseña incorrectos")

    return render_template("authentication/login.html")
