# -*- coding: utf-8 -*-

from nanio import Nanio
from nanio.log import log_root
from nanio.pkg import NODE, UI, DONATE


def main():
    app = Nanio(packages=[DONATE])  # NODE, UI])

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
