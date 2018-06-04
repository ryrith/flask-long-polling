from flask import jsonify, request, Flask
from flask.ctx import copy_current_request_context
import time
import random
import thread

from threading import Thread
polling_data = {}
handlers = {}


def register_handler(operation, fn):
    if not callable(fn):
        raise ValueError('fn must be callable');
    handlers[operation] = fn


def push_update(sid, data, finish=False):
    polling = polling_data.get(sid)
    polling['data'] = data
    polling['updated'] = True
    if finish:
        polling['updated'] = False
        polling['running'] = False


def register(app=None):
    """
    :param app: Flask application object.
    :type app: Flask
    :return:
    """
    if not app:
        from flask import current_app as app


    @app.route('/polling/<sid>')
    def polling_update(sid):
        polling = polling_data.get(sid)
        if not polling:
            return 'Not found!', 404

        while not polling.get('updated'):
            if not polling.get('running'):
                res = jsonify(polling)
                polling['updated'] = True
                break
            time.sleep(0.050)  # second.
        res = jsonify(polling)
        polling['updated'] = False  # it'll be reported by return, so turn off signal
        return res

    @app.route('/polling-start')
    def polling_start():

        args = request.args.to_dict()
        operation = args.get('operation')
        sid = str(random.randint(1000000, 1000000 * 9))
        if sid not in polling_data:
            polling_data[sid] = dict(data=None, updated=False, running=True, sid=sid)
            polling = polling_data.get(sid)
            args['polling'] = polling
            fn = handlers.get(operation) or (lambda: None)
            # this bridging fn that's called in new thread can fully
            # access app_context such as session and request object.
            # Without this decorator, flask will raise error
            # 'RuntimeError: Working outside of request context'
            @copy_current_request_context
            def ctx_bridge():
               fn(**args)
            Thread(target=ctx_bridge).start()
        return jsonify(polling_data.get(sid))

    @app.route('/polling-stop/<sid>')
    def polling_stop(sid):
        polling = polling_data.get(sid)
        polling['updated'] = False
        polling['running'] = False
        polling['data'] = None
        return jsonify(polling)
