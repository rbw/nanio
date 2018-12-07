# -*- coding: utf-8 -*-

from os import environ
from nanio import create_app


def main():
    # Create the app
    app = create_app()
    config = app.cfg.core

    # Run it
    debug = environ.get('NANIO_DEBUG', config['debug'])

    app.run(
        host=environ.get('NANIO_HOST', config['host']),
        port=int(environ.get('NANIO_PORT', config['port'])),
        workers=int(environ.get('NANIO_WORKERS', config['workers'])),
        debug=debug,
        access_log=environ.get('NANIO_ACCESS_LOG', config['access_log'])
    )


if __name__ == '__main__':
    main()
