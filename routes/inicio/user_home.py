from flask import render_template, session, redirect, url_for

def user_home():
    # Verifica si el usuario está logueado
    if "user" not in session:
        return redirect(url_for("login"))

    # Si el usuario es admin, redirige a su panel
    if session.get("is_admin", False):
        return redirect(url_for("admin_home"))

    # Usuario normal, muestra su vista
    return render_template("user/user.html")
