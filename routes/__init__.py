# Principales
from .home import home  
from .obtener_cesta import obtener_cesta  
from .obtener_menu import obtener_menu  

# Contacto
from .contacto import contacto  
from .contacto.contacto_empresa import contacto_empresa  
from .contacto.contacto_particular import contacto_particular  

# Inicio
from .inicio.admin_home import admin_home
from .inicio.user_home import user_home  

# Tienda
from .tienda import encuentranos, nosotros  

# Usuario
from .user.compras import compras  
from .user.informacion_personal import informacion_personal  

# Autenticación
from .authentication.login import login  
from .authentication.olvidado_contraseña import olvidado_contraseña  
from .authentication.registro import registro  
from .authentication.restablecer_contraseña import restablecer_contraseña  
from .authentication.update_contraseña import update_contraseña  
from .authentication.update_usuario import update_usuario
from .authentication.cerrar_sesion import cerrar_sesion  


# Busqueda

from .busqueda import busqueda