import flask
import threading

app = flask.Flask("BatChest")


@app.route("/")
def index():
    return '<html><head><style>body {background-image: url("https://i.redd.it/20iz5ch1hsf71.gif"); background-repeat: repeat; background-color: #000000} h1 {background-color: white;}</style></head><body><h1>You\'ve Been Hax!11!1!!</body></html>'


server = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0"})
server.daemon = True
