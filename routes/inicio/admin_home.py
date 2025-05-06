from flask import render_template, session, redirect, url_for

def admin_home():
    # Verifica si el usuario está logueado
    if "user" not in session:
        return redirect(url_for("login"))

    # Si el usuario no es admin, redirige a su vista
    if not session.get("is_admin", False):
        return redirect(url_for("user_home"))

    # Usuario con rol admin, muestra su vista
    return render_template("admin/admin.html")
