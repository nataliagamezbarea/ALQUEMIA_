from flask_mail import Mail, Message
import os  # Para trabajar con rutas de archivos

mail = Mail()

def enviar_correo(app, asunto, destinatario, cuerpo, archivos=None):
    # Se conecta Flask-Mail con la app
    mail.init_app(app)

    # Se arma el mensaje con el asunto y a quién va
    msg = Message(asunto, recipients=[destinatario])
    msg.body = cuerpo

    # Si hay archivos adjuntos, se agregan al correo
    if archivos:
        for archivo in archivos:
            with app.open_resource(archivo) as adjunto:
                filename = os.path.basename(archivo)  # Solo el nombre del archivo
                msg.attach(filename, "application/octet-stream", adjunto.read())

    # Se envía el correo
    mail.send(msg)
