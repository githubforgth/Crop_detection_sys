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
results = model.train(data='/gth/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)',
                      epochs=300, imgsz=64, device='0')
