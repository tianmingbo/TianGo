# -*- coding: utf-8 -*-
"""
@author:mingbo.tian
@file: main.py
@time: 2024/1/15  20:59
@desc: 
"""
import uvicorn

from dali import app

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
