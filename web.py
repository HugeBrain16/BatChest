"""website module for the bot"""

import threading
import flask
import config

app = flask.Flask("BatChest")


@app.route("/")
def index():
    """bot's index page"""
    return flask.render_template("index.html")


server = threading.Thread(target=app.run, kwargs={"host": config.HOST, "port": config.PORT})
server.daemon = True
