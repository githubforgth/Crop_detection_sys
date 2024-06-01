#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/2/16 下午7:11
# @Author : Gao_Taiheng
# @File : mail.py
# from flask_mail import Mail
# from app import app
# import os
#
# mail = Mail(app)
# app.config['MAIL_SERVER']
s = """3016
3088
2986
3520
2843
4120
2723
2656
3951
3253
3253
2520
3333
3110
3630
3540
3620
3103
3026
2720
2855
3652
3202
2998
3203
3062
3262
3526
3644
3585
3253
3654
3256
3926
2985
3576
3695
3220
3436"""
print(sum(int(i*0.22) + i for i in map(int, s.split('\n'))))