#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/1/8 下午8:18
# @Author : Gao_Taiheng
# @File : train.py
from ultralytics import YOLO

# Load a model
model = YOLO('./runs/classify/train21/weights/best.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='/home/gth/PycharmProjects/Graduation_project/ML/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)', epochs=200, imgsz=64, device='0')
