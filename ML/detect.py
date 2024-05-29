#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/1/10 下午7:37
# @Author : Gao_Taiheng
# @File : detect.py
from flask import Flask
from ultralytics import YOLO

# Load a model
model = YOLO(
    '/home/gth/PycharmProjects/Graduation_project/ML/runs/classify/train23/weights/best.pt')  # pretrained YOLOv8n model


def detect_pic(pic_path: str, model):
    # Process results list
    # res = model(pic_path)[0]
    predict = model.predict(pic_path)  # The result of picture on this model.
    # print(type(res['name']))
    probs = predict[0].probs  # Probs object for classification outputs.
    print(predict[0].names[probs.top1], probs.top1conf.item())
    return {'class_name': predict[0].names[probs.top1],
            'class_prob': '{:.2f}%'.format(probs.top1conf.item() * 100)
            }  # return class name and probability.


if __name__ == '__main__':
    detect_pic("/home/gth/PycharmProjects/Graduation_project/ML/test/test/PotatoEarlyBlight4.JPG", model)
