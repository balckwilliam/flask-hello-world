from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import pexpect
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')
child = pexpect.spawn('/bin/bash')

@socketio.on('input', namespace='/test')
def test_message(message):
    command = message['data']
    child.sendline(command)
    child.expect('\r\n')
    result = child.before.decode('utf-8')
    emit('output', {'data': result})

@app.route('/')
def index():
    return render_template_string("""
        <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.js"></script>
        <script type="text/javascript" charset="utf-8">
            var socket = io.connect('https://' + document.domain + ':' + location.port + '/test');
            socket.on('output', function(msg) {
                document.getElementById('output').value += msg.data + '\\n';
            });
            function send_command() {
                var input = document.getElementById('input');
                socket.emit('input', {data: input.value});
                input.value = '';
            }
        </script>
        <textarea id="output" rows="20" cols="80" readonly="readonly"></textarea><br>
        <input type="text" id="input">
        <button onclick="send_command()">Send</button>
    """)
