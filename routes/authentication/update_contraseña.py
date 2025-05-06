from flask import request, redirect, url_for, session, render_template  # Importamos funciones de Flask
import bcrypt  # Para la encriptación de contraseñas
from backend.base_de_datos import obtener_tabla, db  # Importamos la base de datos y la función para obtener tablas

def update_contraseña():
    # Verificamos si el usuario está logueado.
    Usuario = obtener_tabla("usuarios")  # Obtenemos el modelo de la tabla 'usuarios'

    user_id = session.get("user")  # Intentamos obtener el ID del usuario desde la sesión.
    
    if not user_id:
        # Si no está logueado, redirigimos al login.
        return redirect(url_for("login"))

    # Consultamos al usuario en la base de datos usando su ID
    usuario = db.session.query(Usuario).filter_by(id_usuario=user_id).first()

    if not usuario:
        # Si el usuario no se encuentra, redirigimos al login.
        return redirect(url_for("login"))

    # Inicializamos variables para los mensajes
    mensaje = None
    tipo_mensaje = None

    if request.method == "POST":
        # Recolectamos los datos ingresados por el usuario
        actual = request.form.get("actual")
        nueva = request.form.get("nueva")
        confirmar = request.form.get("confirmar")

        # Verificamos si la contraseña actual es correcta
        if not bcrypt.checkpw(actual.encode('utf-8'), usuario.contrasena.encode('utf-8')):
            mensaje = "La contraseña actual es incorrecta."  # Mensaje de error si la contraseña no es correcta.
            tipo_mensaje = "error"
        # Verificamos si la nueva contraseña y su confirmación coinciden
        elif nueva != confirmar:
            mensaje = "Las contraseñas no coinciden."  # Mensaje de error si no coinciden.
            tipo_mensaje = "error"
        else:
            # Si todo es correcto, encriptamos la nueva contraseña antes de guardarla
            usuario.contrasena = bcrypt.hashpw(nueva.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.session.commit()  # Guardamos los cambios en la base de datos
            mensaje = "Contraseña actualizada correctamente."  # Confirmación de éxito.
            tipo_mensaje = "exito"

    # Renderizamos la plantilla con el mensaje y el tipo de mensaje
    return render_template("user/user_config/cambiar_contraseña.html", mensaje=mensaje, tipo_mensaje=tipo_mensaje)
