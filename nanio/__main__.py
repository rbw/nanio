# -*- coding: utf-8 -*-

from jetfactory import Jetfactory
from jetfactory.pkg import PKG_UI

from nanio.pkg.donate import PKG_DONATE
from nanio.pkg.node import PKG_NODE


def main():
    app = Jetfactory(
        settings_file='settings/core.yml',
        packages=[PKG_UI, PKG_DONATE, PKG_NODE]
    )

    app.log.info('Nanio starting...')

    app.run(
        host=app.config['APP_HOST'],
        port=app.config['APP_PORT'],
        workers=app.config['APP_WORKERS'],
        debug=app.config['APP_DEBUG'],
        access_log=False
    )


if __name__ == '__main__':
    main()
