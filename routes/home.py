from flask import render_template, session, redirect, url_for

def home():
    # Si hay sesión activa
    if "user" in session:
        # Redirige según el tipo de usuario
        if session.get("is_admin"):
            return redirect(url_for("admin_home"))
        return redirect(url_for("user_home"))

    # Si no hay sesión, muestra la página pública
    return redirect(url_for("user_home"))
