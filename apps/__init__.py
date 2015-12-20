#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/19'

from flask import Flask, render_template
from controllers import index


def init_app():
    global app
    app = Flask(__name__)
    app.config.from_object('config')
    register_routes()
    register_log(app)
    return app


def register_routes():
    app.register_blueprint(index.index_bluerint, url_prefix='')


def register_log(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('vansel.log', 'a', 1*1024*1024, 10)
        file_handler.setFormatter(
            logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('server starts successful...')



