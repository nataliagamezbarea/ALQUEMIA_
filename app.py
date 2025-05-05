import os
from flask import Flask
from backend.base_de_datos import init_models  
from routes.home import home

app = Flask(__name__)

# Datos de conexión a la base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/tienda_online'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clave aleatoria para proteger las sesiones del usuario
app.secret_key = os.urandom(24)

# Carga y refleja las tablas de la base de datos
init_models(app)

# Ruta principal de la app
app.add_url_rule('/', 'home', home)

# Lanza la app en modo desarrollo
if __name__ == '__main__':
    app.run(debug=True)
