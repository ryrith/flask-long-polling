#!/usr/bin/env python

from flask import Flask, jsonify, request, render_template
import time, threading, random

app = Flask(__name__)
app.secret_key = 'FUCKING'

@app.route("/")
def main():
    from flask import session
    session['n'] = 100
    return render_template("index.html")


@app.route('/other')
def other_link():
    return 'other link is still work fine'

import polling
import mylogic

# register route & operation
polling.register(app)
polling.register_handler('first_logic', mylogic.first_logic)
polling.register_handler('second_logic', mylogic.second_logic)

# override updaters.
old_updater = mylogic.updater
def new_updater(message,**kwargs):
    old_updater(message=message, **kwargs)
    sid = kwargs.get('polling').get('sid')
    data = message
    finish = kwargs.get('finish') or False
    polling.push_update(sid=sid, data=data, finish=finish)
mylogic.updater = new_updater



if __name__ == "__main__":
    # start server and web page pointing to it
    port = 5000
    app.use_reloader = True
    app.run(port=port, debug=True, threaded=True)
