# coding:utf-8 
__author__ = 'hy'

import logging
import inspect
import os

logging.basicConfig(filename='error.log', level=logging.INFO,
                    format='[%(asctime)s %(levelname)s ] %(message)s ', datefmt='%m/%d/%Y %H:%M:%S')


def log(error):
    target_file, linenum = inspect.stack()[1][1:3]

    target_file = os.path.abspath(target_file)
    basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    target_file_path = target_file.replace(basedir, '')[1:]
    line_info = '[{0}:line{1}],'.format(target_file_path, linenum)

    filename_linenum_errors = logging.info(line_info+error)
    return filename_linenum_errors


