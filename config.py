#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/2/16 下午10:51
# @Author : Gao_Taiheng
# @File : config.py
import os


class Config:
    SECRET_KEY = 'gth'
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')