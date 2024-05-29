#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/2/16 下午10:56
# @Author : Gao_Taiheng
# @File : mail.py
import random


def random_verify_code(length=6):
    return "".join([str(random.randint(0, 10)) for i in range(length)])
