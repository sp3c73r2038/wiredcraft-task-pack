# -*- coding: utf-8 -*-
import argparse
import json
import logging
import pprint
import sys

import flask
import os.path
import redis

LOGGER = logging.getLogger(__name__)

server = flask.Flask(__name__)
CACHE = redis.StrictRedis()
DB = redis.StrictRedis()
CACHE_KEY = 'wiredcraft-task-004-cache'
DB_KEY = 'wiredcraft-task-004-db'

def setupLogging(debug, loggerConfig=None):

    lvl = logging.INFO
    if debug:
        lvl = logging.DEBUG

    root = logging.getLogger()
    root.handlers.clear()
    hdl = logging.StreamHandler(sys.stderr)
    fmt = (
        '[%(asctime)s %(levelname)-7s %(name)s '
        '%(filename)s:%(lineno)d] %(message)s')
    if debug:
        fmt = (
            '[%(asctime)s %(levelname)-7s %(name)s '
            '%(filename)s:%(lineno)d] ===\n%(message)s')
    f = logging.Formatter(fmt)
    hdl.setFormatter(f)
    root.setLevel(lvl)
    root.addHandler(hdl)

    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('gunicorn').setLevel(logging.WARNING)
    logging.getLogger('elasticsearch').setLevel(logging.WARNING)

    if loggerConfig:
        for k, v in loggerConfig.items():
            logging.getLogger(k).setLevel(v)

@server.route('/')
def index():
    return flask.jsonify({'msg': 'hello'})

@server.route('/welcome')
def read():
    """
    /welcome read API
    """
    # read from cache first
    name = CACHE.get(CACHE_KEY)
    cacheHit = 'Hit'
    if not name:
        # read from database if cache miss
        cacheHit = 'Miss'
        name = DB.get(DB_KEY)
        # don't forget to set cache
        CACHE.setex(CACHE_KEY, server.config['CACHE_TTL'], name)

    name = name.decode()

    resp = flask.make_response('Hello, {}'.format(name))
    resp.headers['X-CACHE'] = cacheHit
    return resp

@server.route('/welcome', methods=['PUT'])
def write():
    """
    /welcome write API
    """
    ct = flask.request.headers.get('Content-Type')
    if ct != 'application/json':
        return flask.abort(
            400, 'invalid Content-Type, should be application/json')

    data = json.loads(flask.request.data)

    if not isinstance(data, dict) or not data.get('name'):
        return flask.abort(400, 'missing args name or invalid data type')

    name = str(data.get('name'))

    # write database
    DB.set(DB_KEY, name)

    # set cache
    CACHE.setex(CACHE_KEY, server.config['CACHE_TTL'], name)

    return flask.jsonify({'msg': 'update ok'})

def main():
    global CACHE, DB

    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--config', default='config.py')
    ap.add_argument('--local-config', default='config_local.py')
    ap.add_argument('--bind', default='0.0.0.0')
    ap.add_argument('--port', default=3000, type=int)

    options = ap.parse_args()

    setupLogging(options.debug)

    # load config file
    LOGGER.info(">> load config from %s", options.config)
    server.config.from_pyfile(options.config)

    # load custom config if exists
    if os.path.isfile(options.local_config):
        LOGGER.info(">> load config from %s", options.local_config)
        server.config.from_pyfile(options.local_config)

    LOGGER.info("--- options: \n%s", pprint.pformat(options))
    LOGGER.info("--- config: \n%s", pprint.pformat(server.config))

    # setup redis cache
    CACHE = redis.StrictRedis.from_url(
        server.config['CACHE_REDIS_URL'], socket_timeout=10)

    # setup redis db
    DB = redis.StrictRedis.from_url(
        server.config['DB_REDIS_URL'], socket_timeout=10)

    # write data into database
    LOGGER.info(">> initialize data into database")
    DB.set(DB_KEY, 'John Doe')

    server.run(options.bind, port=options.port, threaded=True)

if __name__ == '__main__':
    main()
