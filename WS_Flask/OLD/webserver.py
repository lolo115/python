from WS_flask import Flask

app = Flask (__name__)


@app.route ("/")
def index():
    return "Hello U"


@app.route ("/members/<string:name>/")
def getMember(name):
    return name


if __name__ == "__main__":
    app.run (host="127.0.0.1", port=80)