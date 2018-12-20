# -*- coding: utf-8 -*-

from nanio import create_app
from nanio.log import log_root


def main():
    app = create_app()

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
