from flask import Flask

version = b"0.1.0"
app = Flask(__name__)

@app.route("/")
def hello():
    return version

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)