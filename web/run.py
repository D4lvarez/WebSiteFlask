from WebSite import create_app
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from WebSite.models import Chat


app = create_app()
db = SQLAlchemy(app)
socketio = SocketIO(app)

db.init_app(app)

# Recibirá los nuevos mensajes y los emitirá por socket
@socketio.on('new_message')
def new_message(message):
    # Emitimos el mensaje con el alias y el mensaje del usuario
    emit('new_message', {
        'username': message['username'],
        'text': message['text']
    }, broadcast=True)
    # Salvamos el mensaje en la base de datos
    my_new_chat = Chat(
        username=message['username'],
        text=message['text']
    )
    db.session.add(my_new_chat)
    db.session.commit()


if __name__ == '__main__':
    socketio.run(app, debug=True, host="50.190.180.86")
