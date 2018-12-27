# -*- coding: utf-8 -*-

# from jetfactory.
from nanio import Nanio
from nanio.log import log_root
from nanio.pkg.donate import PKG_DONATE
from nanio.pkg.node import PKG_NODE


def main():
    app = Nanio(packages=[PKG_DONATE, PKG_NODE, PKG_UI])

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
