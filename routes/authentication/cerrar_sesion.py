from flask import redirect, url_for, session

def cerrar_sesion():
    # Elimina al usuario de la sesión si está logueado
    session.pop("user", None)

    # También borra el estado de administrador si existía
    session.pop("is_admin", None)

    # Redirige al login después de cerrar sesión
    return redirect(url_for("login"))
