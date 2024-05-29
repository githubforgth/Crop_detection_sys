#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/2/16 下午7:11
# @Author : Gao_Taiheng
# @File : mail.py
from flask_mail import Mail
from app import app
import os

mail = Mail(app)
app.config['MAIL_SERVER']
