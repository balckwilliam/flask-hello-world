from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_cmd', methods=['POST'])
def run_cmd():
    command = request.form['command']
    try:
        output = subprocess.check_output(command, shell=True)
        return jsonify({'output': output.decode('utf-8')})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': str(e)})
