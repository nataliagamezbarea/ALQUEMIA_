from flask import render_template, request, current_app
from routes.authentication.enviar_correo import enviar_correo
from routes.authentication.tokens import obtener_clave_secreta
from backend.base_de_datos import obtener_tabla, db
from sqlalchemy.orm import Session  # Importación necesaria

def olvidado_contraseña():
    mensaje = None
    tipo_mensaje = None

    if request.method == "POST":
        correo = request.form['email']

        # Carga el modelo reflejado
        Usuario = obtener_tabla('usuarios')

        # Crea una sesión de base de datos
        session_db = Session(db.engine)

        # Busca el usuario por email
        usuario_encontrado = session_db.query(Usuario).filter_by(email=correo).first()

        if usuario_encontrado:
            # Genera token para el correo
            s = obtener_clave_secreta()
            token = s.dumps(correo, salt='password-reset-salt')

            url_restablecer = f"http://localhost:5000/restablecer_contraseña/{token}"
            cuerpo = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {url_restablecer}'

            # Envía el correo
            enviar_correo(current_app, "Restablecimiento de Contraseña", correo, cuerpo)

            mensaje = "Correo enviado. Revisa tu bandeja de entrada."
            tipo_mensaje = "exito"
        else:
            mensaje = "No se encontró una cuenta asociada a ese correo."
            tipo_mensaje = "error"

        session_db.close()  # Cierra la sesión

    return render_template('authentication/olvidado_contraseña.html', mensaje=mensaje, tipo_mensaje=tipo_mensaje)
