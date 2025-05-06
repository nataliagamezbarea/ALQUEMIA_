import os
from flask import Flask
from backend.base_de_datos import db, init_models

# Importamos las funciones para las vistas
from routes.authentication  import login , olvidado_contraseña ,  registro , restablecer_contraseña
from routes import home
from routes.inicio import admin_home , user_home

app = Flask(__name__)

# Configuramos los datos para enviar correos (esto se toma desde variables de entorno)
app.config.update(
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_USE_TLS=os.getenv("MAIL_USE_TLS"),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER")
)

# Esta clave es para poder usar sesiones seguras dentro de Flask
app.secret_key = os.urandom(24)

# Datos de conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/tienda_online'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Carga y refleja las tablas de la base de datos
init_models(app)

# Ruta principal de la app
app.add_url_rule("/", "home", home)
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/registro", "registro", registro, methods=["GET", "POST"])
app.add_url_rule("/olvidado_contraseña", "olvidado_contraseña", olvidado_contraseña, methods=["GET", "POST"])
app.add_url_rule("/restablecer_contraseña/<token>", "restablecer_contraseña", restablecer_contraseña, methods=["GET", "POST"])


# Panel de administrador
app.add_url_rule("/admin", "admin_home", admin_home)
app.add_url_rule("/user", "user_home", user_home)

# Lanza la app en modo desarrollo
if __name__ == "__main__":
    app.run(debug=True)
