import secrets
from itsdangerous import URLSafeTimedSerializer

# Esta clave se genera al iniciar el servidor y se usa para firmar los tokens.
# Como se genera dinámicamente, los tokens anteriores se invalidan si se reinicia el servidor.
clave_secreta = secrets.token_urlsafe(32)

def obtener_clave_secreta():
    # Retorna un serializador que permite crear y verificar tokens seguros y con expiración
    return URLSafeTimedSerializer(clave_secreta)
