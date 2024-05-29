#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/1/2 下午9:37
# @Author : Gao_Taiheng
# @File : test.py


# srcfile 需要复制、移动的文件
# dstpath 目的地址

import os
import shutil

src_path = "/home/gth/PycharmProjects/Graduation_project/ML/data/archive/image/Dataset/train/"
tar_path = "/home/gth/PycharmProjects/Graduation_project/ML/data/JPEGImages"

for i in os.listdir(src_path):
    for j in os.listdir(src_path + i + "/"):
        src_file = os.path.join(src_path, i, j)
        dst_file = os.path.join(tar_path, j)
        shutil.copy(src_file, dst_file)
