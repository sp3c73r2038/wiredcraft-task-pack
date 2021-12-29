# -*- coding: utf-8 -*-
import argparse
import json
import logging
import pprint
import sys
import time

import flask
import os.path
import redis

LOGGER = logging.getLogger(__name__)

server = flask.Flask(__name__)
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


class ICache:
    """
    Cache Interface
    """
    def get(self, k):
        raise NotImplementedError()
    def put(self, k, v, expiry):
        raise NotImplementedError()

class IDatabase:
    """
    Database Interface
    """
    def get(self, k):
        raise NotImplementedError()
    def put(self, k, v):
        raise NotImplementedError()

class MemoryCache:
    """
    In-Memory Cache Implementation, for testing purpose
    """
    def __init__(self):
        self.store = {}

    def get(self, k):
        d = self.store.get(k)
        if d and d['timestamp'] >= time.time():
            return d['data']

    def put(self, k, v, expiry=None):
        ts = 1e10
        if expiry:
            ts = time.time() + expiry
        d = {
            'timestamp': ts,
            'data': v
        }
        self.store[k] = d

class MemoryDB:
    """
    In-Memory Database Implementation, for testing purpose
    """
    def __init__(self):
        self.store = {}

    def get(self, k):
        return self.store.get(k)

    def put(self, k, v):
        self.store[k] = v

class RedisCache:
    """
    Cache Implementation using Redis
    """
    def __init__(self, url, socket_timeout=10):
        self.client = redis.StrictRedis.from_url(
            url, socket_timeout=socket_timeout)

    def get(self, k):
        return self.client.get(k)

    def put(self, k, v, expiry=None):
        if expiry:
            self.client.setex(k, expiry, v)
        else:
            self.client.set(k, v)

class RedisDB:
    """
    DB Implementation using Redis
    """
    def __init__(self, url, socket_timeout=10):
        self.client = redis.StrictRedis.from_url(
            url, socket_timeout=socket_timeout)

    def get(self, k):
        return self.client.get(k)

    def put(self, k, v):
        self.client.set(k, v)


CACHE = ICache()
DB = IDatabase()
CACHE_KEY = 'wiredcraft-task-004-cache'
DB_KEY = 'wiredcraft-task-004-db'

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
        CACHE.put(CACHE_KEY, name, server.config['CACHE_TTL'])

    if isinstance(name, bytes):
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

    try:
        data = json.loads(flask.request.data)
    except ValueError:
        return flask.abort(400, 'invalid JSON')

    if not isinstance(data, dict) or not data.get('name'):
        return flask.abort(400, 'missing args name or invalid data type')

    name = str(data.get('name'))

    # write database
    DB.put(DB_KEY, name)

    # set cache
    CACHE.put(CACHE_KEY, name, server.config['CACHE_TTL'])

    return flask.jsonify({'msg': 'update ok'})

def init():
    """
    setup cache and database
    """
    global CACHE, DB
    if server.config['UNIT_TEST']:
        # use in-memory implementation for testing purpose
        CACHE = MemoryCache()
        DB = MemoryDB()
    else:
        CACHE = RedisCache(server.config['CACHE_REDIS_URL'])
        DB = RedisDB(server.config['DB_REDIS_URL'])

    # write data into database
    LOGGER.info(">> initialize data into database")
    DB.put(DB_KEY, 'John Doe')

def main():

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

    # init global context
    init()

    server.run(options.bind, port=options.port, threaded=True)

if __name__ == '__main__':
    main()
