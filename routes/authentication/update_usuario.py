from flask import request, redirect, url_for, session, render_template
from backend.base_de_datos import db, obtener_tabla

def update_usuario():
    # Intento obtener el ID del usuario que está actualmente en sesión
    user_id = session.get("user")
    
    # Si no hay un usuario logueado, redirijo a la página de inicio de sesión
    if not user_id:
        return redirect(url_for("login"))

    # Obtengo el modelo correspondiente a la tabla 'usuarios'
    Usuario = obtener_tabla("usuarios")

    # Busco al usuario dentro de la base de datos usando el ID obtenido de la sesión
    usuario = db.session.query(Usuario).filter_by(id_usuario=user_id).first()
    
    # Si no se encuentra al usuario, devuelvo un mensaje de error
    if not usuario:
        return render_template("error.html", mensaje="Usuario no encontrado", tipo_mensaje="error")

    # Si es una solicitud POST, actualizo los datos del usuario
    if request.method == "POST":
        # Recojo los datos del formulario
        nombre = request.form.get("nombre")
        apellido1 = request.form.get("apellido1")
        apellido2 = request.form.get("apellido2")
        email = request.form.get("email")

        # Validación de los datos ingresados
        if not nombre or not apellido1 or not apellido2 or not email:
            return render_template("error.html", mensaje="Todos los campos son obligatorios.", tipo_mensaje="error")

        # Asigno los nuevos valores al objeto usuario
        usuario.nombre = nombre
        usuario.apellido1 = apellido1
        usuario.apellido2 = apellido2
        usuario.email = email

        # Guardo los cambios en la base de datos
        db.session.commit()

        # Finalmente, redirijo al usuario a la página de información personal actualizada
        return redirect(url_for("informacion_personal"))

    # Si no es un POST (GET por ejemplo), renderizo el formulario con los datos actuales del usuario
    return render_template('user/user_config/actualizar_usuario.html', usuario=usuario)
