# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: gunicorn_launcher.py
@time: 2024/2/3  16:50
@desc: Gunicorn启动flask
"""

# gunicorn_launcher.py

from gunicorn.app.base import BaseApplication
from test import app


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    options = {
        'bind': '127.0.0.1:8000',
        'workers': 4,
    }
    StandaloneApplication(app, options).run()
