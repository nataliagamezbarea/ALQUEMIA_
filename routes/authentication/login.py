from flask import redirect, render_template, request, session, url_for
import bcrypt
from sqlalchemy.orm import Session
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


        usuario = db.session.query(Usuario).filter_by(email=email).first()

        if usuario and bcrypt.checkpw(contrasena.encode("utf-8"), usuario.contrasena.encode("utf-8")):
            session["user"] = usuario.id_usuario
            session["is_admin"] = getattr(usuario, "is_admin", False)
            db.session.close()

            if session["is_admin"]:
                return redirect(url_for("admin_home"))
            return redirect(url_for("user_home"))
        else:
            db.session.close()
            return render_template("authentication/login.html", error="Email o contraseña incorrectos")

    return render_template("authentication/login.html")
