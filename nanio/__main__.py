# -*- coding: utf-8 -*-

from nanio import Nanio
from nanio.log import log_root
from nanio.pkg.node import NODE
from nanio.pkg.donate import DONATE
from nanio.pkg.ui import UI


def main():
    app = Nanio(packages=[NODE, UI, DONATE])

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
