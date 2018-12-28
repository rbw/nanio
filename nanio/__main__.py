# -*- coding: utf-8 -*-

from jetfactory import Jetfactory

from nanio.pkg.donate import PKG_DONATE
from nanio.pkg.node import PKG_NODE
from nanio.pkg.ui import PKG_UI


def main():
    app = Jetfactory(
        packages=[PKG_UI, PKG_DONATE, PKG_NODE],
        settings={
            'TESTAR': ['asd', 'dsa']
        }
    )

    app.log.info('Nanio starting...')
    app.run()


if __name__ == '__main__':
    main()
