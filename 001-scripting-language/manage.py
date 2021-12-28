# -*- coding: utf-8 -*-
import argparse
import datetime
import logging
import pprint
import sys
from threading import Thread
from util import sh

LOGGER = logging.getLogger(__name__)

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

def new(options):
    ptn = 'content/post/%Y_%m_%d_%H_%M_%S_random-post.md'
    dt = datetime.datetime.now()
    filename = dt.strftime(ptn)
    _, content, _ = sh(options.fortune)

    header = dt.strftime(
        '---\ndate: "%Y-%m-%d"\ntitle: '
        '"new post title %Y-%m-%d"\n---\n')

    with open(filename, 'wb') as f:
        f.write(header.encode())
        f.write(b'\n'.join(content))
    LOGGER.info("!! a new post has been created: %s", filename)

def build(options):
    sh(options.hugo)

def preview(options):
    build(options)
    cmd = '{} server --bind {} --port {}'.format(
        options.hugo, options.bind, options.port)
    sh(cmd)

def push(options):
    sh('git add content/post')
    sh('git commit -m "new post"')
    sh('git push origin master')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', action='store_true')
    ap.add_argument('--fortune', default='fortune')
    ap.add_argument('--hugo', default='hugo')
    sub = ap.add_subparsers(dest='cmd', required=False)
    subpreview = sub.add_parser('preview')
    subbuild = sub.add_parser('build')
    subnew = sub.add_parser('new')
    subpush = sub.add_parser('push')

    # preview
    subpreview.add_argument('--bind', default='127.0.0.1')
    subpreview.add_argument('--port', default=1313, type=int)

    options = ap.parse_args()

    setupLogging(options.debug)

    if options.cmd == 'new':
        new(options)
    elif options.cmd == 'build':
        build(options)
    elif options.cmd == 'preview':
        preview(options)
    elif options.cmd == 'push':
        push(options)
    else:
        ap.print_help(sys.stderr)

if __name__ == '__main__':
    main()
