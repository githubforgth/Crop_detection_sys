#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2023/12/28 下午4:34
# @Author : Gao_Taiheng
# @File : Just_test.py
import json
import os

# t = os.listdir("./ML/data/New_Plant_Diseases_Dataset(Augmented)/New_Plant_Diseases_Dataset(Augmented)/train")
# print(t, len(t))

with open("./ML/data/ImageSets/Main/val.txt", "a") as train:
    with open("./ML/data/New_Plant_Diseases Dataset(Augmented)/New_Plant_Diseases_Dataset(Augmented)/val.txt", "r") as f:
        train.write(f.read())
    with open("./ML/data/new_plant_diseases_dataset(augmented)/New_Plant_Diseases_Dataset(Augmented)/val.txt", "r") as f:
        train.write(f.read())