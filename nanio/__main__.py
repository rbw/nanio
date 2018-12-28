# -*- coding: utf-8 -*-

from jetfactory import Jetfactory, JetfactorySettings

from nanio.pkg import pkg_ui, pkg_donate, pkg_node


def main():
    app = Jetfactory(
        packages=[pkg_ui, pkg_node, pkg_donate],
        settings=JetfactorySettings.yaml_to_jet('core.yml')
    )

    app.log.info('Nanio starting...')
    app.run()


if __name__ == '__main__':
    main()
