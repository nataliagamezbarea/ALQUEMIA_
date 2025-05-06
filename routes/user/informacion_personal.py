from flask import render_template, session, redirect, url_for
from sqlalchemy.orm import sessionmaker

from backend.base_de_datos import obtener_tabla, db  # Asegúrate de que db es la instancia de SQLAlchemy

def informacion_personal():
    # Obtener el modelo de Usuario
    Usuario = obtener_tabla('usuarios')
    
    # Verificar si el usuario está logueado
    user_id = session.get("user")

    if not user_id:
        # Si no está logueado, redirigimos al login
        return redirect(url_for("login"))

    # Consultar al usuario con el ID obtenido de la sesión
    usuario = db.session.query(Usuario).filter_by(id_usuario=user_id).first()

    # Si no se encuentra el usuario, redirigimos al login o mostramos error
    if not usuario:
        # Si el usuario no se encuentra en la base de datos, redirigimos al login
        return redirect(url_for("login"))  

    # Si todo es correcto, renderizamos la plantilla y pasamos los datos del usuario
    return render_template('user/user_config/informacion_personal.html', usuario=usuario)
