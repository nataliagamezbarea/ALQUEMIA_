# Importamos las herramientas necesarias para mostrar plantillas, manejar formularios y acceder a la app actual
from flask import render_template, request, current_app

# Importamos la función que se encarga de enviar correos electrónicos
from routes.authentication.enviar_correo import enviar_correo

def contacto_empresa():
    # Inicializamos las variables para mostrar un mensaje al usuario después de enviar el formulario
    mensaje = None
    tipo_mensaje = None

    # Verificamos si el formulario fue enviado con el método POST
    if request.method == 'POST':
        # Recogemos todos los datos que el usuario escribió en el formulario
        nombre = request.form['nombre']
        apellido1 = request.form['apellido1']
        apellido2 = request.form['apellido2']
        email = request.form['email']
        telefono = request.form['telefono']
        tiquet = request.form['tiquet']
        comentario = request.form['comentario']
        opcion = request.form['opcion']

        # El asunto del correo será la opción que eligió el usuario en el formulario
        asunto = opcion 

        # Creamos el contenido del correo con los datos del formulario
        cuerpo = f"""
        Nombre: {nombre} {apellido1} {apellido2}
        Email: {email}
        Teléfono: {telefono}
        Nº tiquet/Pedido: {tiquet}
        Comentario: {comentario}
        """

        # Indicamos la dirección de correo a la que se enviará el mensaje
        destino = "tiendaalquemiaempresa@gmail.com"

        # Usamos la función para enviar el correo con los datos que se recogieron
        enviar_correo(current_app, asunto, destino, cuerpo)

        # Indicamos que el mensaje fue enviado correctamente para mostrarlo en pantalla
        mensaje = "El mensaje se ha enviado correctamente."
        tipo_mensaje = "exito"

        # Mostramos la misma página de contacto con el mensaje de confirmación
        return render_template('contacto/contacto.html', mensaje=mensaje, tipo_mensaje=tipo_mensaje)

    # Si el usuario solo está viendo la página (no envió nada), se muestra el formulario vacío
    return render_template('contacto/contacto.html')
