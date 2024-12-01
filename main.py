from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from urllib.parse import quote  # Use this instead of deprecated `url_quote`

app = Flask(__name__)
app.config['SECRET_KEY'] = '3f82bc47a95f40c3b94e5a7f25d83cf649a2f8bdc22b6e34'
socketio = SocketIO(app)

@app.route('/<room_id>')
def room(room_id):
    return render_template('chat.html', room_id=quote(room_id))

@socketio.on('joinRoom')
def handle_join_room(data):
    room = data.get('roomId')
    if room:
        join_room(room)
        print(f"Client joined room: {room}")

@socketio.on('sendMessage')
def handle_message(data):
    room = data.get('roomId')
    message = data.get('message')
    avatar = data.get('avatar', 'https://iili.io/20rvmEN.md.jpg')  # Default avatar

    if room and message:
        print(f"Message received in room {room}: {message}")
        emit('receive_message', {'message': message, 'avatar': avatar}, room=room, include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
