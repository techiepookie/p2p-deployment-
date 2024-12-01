from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit

# Initialize Flask app and configure SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = '3f82bc47a95f40c3b94e5a7f25d83cf649a2f8bdc22b6e34'  # Replace 'your_secret_key' with a secure key
socketio = SocketIO(app)

# Define the route for chat rooms
@app.route('/<room_id>')
def room(room_id):
    return render_template('chat.html', room_id=room_id)

# Handle joining a chat room
@socketio.on('joinRoom')
def handle_join_room(data):
    room = data.get('roomId')
    if room:
        join_room(room)
        print(f"Client joined room: {room}")

# Handle sending and broadcasting messages
@socketio.on('sendMessage')
def handle_message(data):
    room = data.get('roomId')
    message = data.get('message')
    avatar = data.get('avatar', 'https://iili.io/20rvmEN.md.jpg')  # Default avatar

    if room and message:
        print(f"Message received in room {room}: {message}")
        # Broadcast the message to all users in the room (excluding the sender)
        emit('receive_message', {'message': message, 'avatar': avatar}, room=room, include_self=False)

# Main entry point
if __name__ == '__main__':
    # Run the app, making it accessible on Render or any hosting platform
    socketio.run(app, host='0.0.0.0', port=4000, debug=True)
