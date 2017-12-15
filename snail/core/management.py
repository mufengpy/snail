# coding:utf-8
__author__ = 'hy'

from snail.servers import Server
from snail import IP_PORT
from snail.db import create_table, drop_table
from snail.logger import log

import sys


def execute():
    if len(sys.argv) == 1:
        from snail.form import Tyrion
        Tyrion.setup('snail')
        Server(IP_PORT).run()

    else:
        if sys.argv[0] == 'manage.py':
            if sys.argv[1] == 'migrate':
                try:
                    create_table()
                except Exception as e:
                    print(e)
                    log(e)
                    sys.exit(0)
                else:
                    out = 'all table migrate'
                    print(out)
                    log(out)
            if sys.argv[1] == 'drop':
                try:
                    drop_table()
                except Exception as e:
                    print(e)
                    log(e)
                    sys.exit(0)
                else:
                    out = 'all table droped'
                    print(out)
                    log(out)
            sys.exit(0)