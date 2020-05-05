from gevent import monkey; monkey.patch_all()
import gevent

import sqlite3

from gevent import pywsgi

from metweb import app

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("db_file", help="Database file")
    args = parser.parse_args()

    dbc = sqlite3.connect(args.db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    app = app.create_app(dbc)

    server = gevent.pywsgi.WSGIServer(('0.0.0.0', 8888), app)
    server.serve_forever()
