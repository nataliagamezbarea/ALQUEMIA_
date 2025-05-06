from flask import redirect, render_template, request, session, url_for
import bcrypt
from sqlalchemy.orm import sessionmaker
from backend.base_de_datos import db, obtener_tabla

def login():
    Usuario = obtener_tabla("usuarios")  # Modelo reflejado directamente aquí

    # Si ya hay sesión activa, redirige según tipo de usuario
    if "user" in session:
        if session.get("is_admin"):
            return redirect(url_for("admin_home"))
        return redirect(url_for("user_home"))

    if request.method == "POST":
        email = request.form.get("email")
        contrasena = request.form.get("contrasena")

        # Realizamos la consulta correctamente usando db.session.query()
        usuario = db.session.query(Usuario).filter_by(email=email).first()

        # Verificamos si el usuario existe y si la contraseña es correcta
        if usuario and bcrypt.checkpw(contrasena.encode("utf-8"), usuario.contrasena.encode("utf-8")):
            session["user"] = usuario.id_usuario  # Guardamos el ID del usuario en la sesión
            session["is_admin"] = getattr(usuario, "is_admin", False)  # Guardamos si es admin

            # Redirigimos según si es admin o usuario común
            if session["is_admin"]:
                return redirect(url_for("admin_home"))
            return redirect(url_for("user_home"))
        else:
            # Si las credenciales no son correctas, mostramos un mensaje de error
            return render_template("authentication/login.html", error="Email o contraseña incorrectos")

    return render_template("authentication/login.html")
