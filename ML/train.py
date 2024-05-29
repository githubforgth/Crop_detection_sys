#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/1/8 下午8:18
# @Author : Gao_Taiheng
# @File : train.py
from ultralytics import YOLO
import torch

print(torch.cuda.is_available())
# Load a model
model = YOLO('./runs/classify/train22/weights/best.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='/home/gth/Desktop/毕业设计/archive/New Plant Diseases Dataset(Augmented)/New Plant Diseases '
                           'Dataset(Augmented)/',
                      epochs=100, imgsz=320, device='0', cos_lr=True, workers=16,
                      project="../run/train1")
