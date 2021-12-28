# -*- coding: utf-8 -*-
import io
import logging
from queue import Empty, Queue
import subprocess
from subprocess import Popen, PIPE
import sys
from threading import Thread
import pprint


LOGGER = logging.getLogger(__name__)

def cb(line):
    print(line.decode(), end='')

def sh(cmd, echo=True, loud=False, outCallback=None, errCallback=None):
    def enqueue_data(out, queue):
        for c in iter(out.readline, b''):
            queue.put(c)
        out.close()

    outq = Queue()
    errq = Queue()

    out = []
    err = []

    LOGGER.info(">> sh cmd: %s", cmd)

    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    t1 = Thread(target=enqueue_data, args=(p.stdout, outq))
    t1.daemon = True
    t1.start()
    t2 = Thread(target=enqueue_data, args=(p.stderr, errq))
    t2.daemon = True
    t2.start()

    def drainPipe(q, tgt, cb, defout):
        while True:
            try:
                # drain queue util empty
                line = q.get(timeout=.05)
                tgt.append(line)
                if callable(cb):
                    # call cb if not None
                    cb(line)
                else:
                    # or via default output
                    print(line.decode(), flush=True, file=defout, end='')
            except Empty:
                return

    while True:
        rc = p.poll()
        if rc is not None:
            # sub process ended
            if loud and rc != 0:
                raise subprocess.CalledProcessError(rc, cmd)
            break

        # read stdout
        drainPipe(outq, out, outCallback, sys.stdout)

        # read stderr
        drainPipe(errq, err, errCallback, sys.stderr)

    t1.join()
    t2.join()

    # read stdout
    drainPipe(outq, out, outCallback, sys.stdout)

    # read stderr
    drainPipe(errq, err, errCallback, sys.stderr)

    return rc, out, err

def main():
    rt = sh('for i in $(seq 1 5); do date; sleep 1; done', loud=True)
    pprint.pprint(rt)

if __name__ == '__main__':
    main()
