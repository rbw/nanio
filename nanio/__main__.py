# -*- coding: utf-8 -*-

from jetfactory import Jetfactory, utils
from jetfactory.pkg.example import pkg_example
from jetfactory.pkg import pkg_ui
from nanio.pkg import pkg_donate, pkg_node


def main():
    app = Jetfactory(
        packages=[pkg_example, pkg_ui],  # [pkg_ui, pkg_node, pkg_donate, pkg_oauth],
        settings=utils.yaml_parse('core.yml', keys_to_upper=True)
    )

    app.log.info('Nanio starting...')
    app.run()


if __name__ == '__main__':
    main()
