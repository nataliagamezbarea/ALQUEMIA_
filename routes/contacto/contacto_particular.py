# Importamos lo necesario para renderizar la plantilla, recibir datos del formulario y usar la configuración de la app
from flask import render_template, request, current_app

# Importamos la función que envía correos, ya definida en otro archivo
from routes.authentication.enviar_correo import enviar_correo

def contacto_particular():
    # Inicializamos variables para guardar el mensaje que se mostrará al usuario
    mensaje = None
    tipo_mensaje = None

    # Verificamos si el usuario envió el formulario (usando el método POST)
    if request.method == 'POST':
        # Guardamos los datos que el usuario escribió en el formulario
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        email = request.form['email']
        telefono = request.form['telefono']
        tiquet = request.form['tiquet']
        comentario = request.form['comentario']
        opcion = request.form['opcion']  # Esta opción define el motivo de contacto

        # Usamos la opción elegida por el usuario como asunto del correo
        asunto = opcion 

        # Creamos el cuerpo del mensaje con los datos proporcionados por el usuario
        cuerpo = f"""
        Nombre: {nombre} {apellido1} {apellido2}
        Email: {email}
        Teléfono: {telefono}
        Nº tiquet/Pedido: {tiquet}
        Comentario: {comentario}
        """

        # Definimos la dirección de correo a la que se enviará el mensaje
        destino = "tiendaalquemiaparticular@gmail.com"

        # Enviamos el correo usando la función configurada previamente
        enviar_correo(current_app, asunto, destino, cuerpo)

        # Mostramos un mensaje al usuario indicando que todo fue exitoso
        mensaje = "El mensaje se ha enviado correctamente."
        tipo_mensaje = "exito"

        # Renderizamos la plantilla con el mensaje de éxito incluido
        return render_template('contacto/contacto.html', mensaje=mensaje, tipo_mensaje=tipo_mensaje)

    # Si el formulario aún no se ha enviado, simplemente mostramos la página vacía
    return render_template('contacto/contacto.html')
