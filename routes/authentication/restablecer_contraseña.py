import bcrypt
from flask import render_template, request, redirect, url_for
from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy.orm import Session

from routes.authentication.tokens import obtener_clave_secreta
from backend.base_de_datos import obtener_tabla, db

def restablecer_contraseña(token):
    # Crear un serializador para verificar el token
    s = obtener_clave_secreta()

    try:
        # Intenta recuperar el correo desde el token (válido por 1 hora)
        correo = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return "El enlace ha expirado.", 400
    except BadSignature:
        return "El enlace no es válido.", 400

    # Obtener la tabla reflejada de usuarios
    Usuario = obtener_tabla('usuarios')

    if request.method == "POST":
        nueva_contraseña = request.form.get("nueva_contraseña")

        if nueva_contraseña:
            # Crear una sesión de base de datos usando el motor de SQLAlchemy
            session = Session(db.engine)

            try:
                usuario = session.query(Usuario).filter_by(email=correo).first()

                if usuario:
                    # Encriptar la nueva contraseña
                    hash_pw = bcrypt.hashpw(nueva_contraseña.encode("utf-8"), bcrypt.gensalt())
                    usuario.contrasena = hash_pw.decode("utf-8")
                    session.commit()
                    return redirect(url_for("login"))
            finally:
                session.close()

    # Mostrar el formulario si es GET o si ocurrió un error
    return render_template("authentication/restablecer_contraseña.html", token=token)
