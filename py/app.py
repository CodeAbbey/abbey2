from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hi, People!!!'

app.run(host='0.0.0.0', port=5000, debug=True)
