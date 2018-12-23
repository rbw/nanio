# -*- coding: utf-8 -*-

from nanio import Nanio
from nanio.log import log_root
from nanio.ext.node import NODE
from nanio.ext.donation import DONATION


def main():
    app = Nanio([NODE, DONATION])

    log_root.info('Nanio starting...')

    app.run(
        host=app.config['APP_HOST'],
        port=app.config['APP_PORT'],
        workers=app.config['APP_WORKERS'],
        debug=app.config['APP_DEBUG'],
        access_log=False
    )


if __name__ == '__main__':
    main()
