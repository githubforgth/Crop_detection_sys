#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/5/29 上午10:18
# @Author : Gao_Taiheng
# @File : plot.py
import pandas as pd
import matplotlib.pyplot as plt


def plot_training_results(csv_file1, csv_file2):
    # Read CSV into DataFrames
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    print(df1.keys())
    print(df2.keys())

    # Extract data from DataFrames
    epochs1 = df1['                  epoch']
    train_loss1 = df1['             train/loss']
    train_accuracy_top11 = df1['  metrics/accuracy_top1']
    train_accuracy_top51 = df1['  metrics/accuracy_top5']
    val_loss1 = df1['               val/loss']
    lr_pg01 = df1['                 lr/pg0']
    lr_pg11 = df1['                 lr/pg1']
    lr_pg21 = df1['                 lr/pg2']

    epochs2 = df2['                  epoch']
    train_loss2 = df2['             train/loss']
    train_accuracy_top12 = df2['  metrics/accuracy_top1']
    train_accuracy_top52 = df2['  metrics/accuracy_top5']
    val_loss2 = df2['               val/loss']
    lr_pg02 = df2['                 lr/pg0']
    lr_pg12 = df2['                 lr/pg1']
    lr_pg22 = df2['                 lr/pg2']

    # Plotting
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(epochs1, train_loss1, marker='o', label='YOLOv8')
    plt.plot(epochs2, train_loss2, marker='x', label='YOLOv8+attention')
    plt.xlabel('Epoch')
    plt.ylabel('Train Loss')
    plt.title('Train Loss')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(epochs1, train_accuracy_top11, marker='o', label='YOLOv8')
    plt.plot(epochs2, train_accuracy_top12, marker='x', label='YOLOv8+attention')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy Top 1')
    plt.title('Top 1 Accuracy')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(epochs1, val_loss1, marker='o', label='YOLOv8')
    plt.plot(epochs2, val_loss2, marker='x', label='YOLOv8+attention')
    plt.xlabel('Epoch')
    plt.ylabel('Validation Loss')
    plt.title('Validation Loss')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(epochs1, train_accuracy_top51, marker='o', label='YOLOv8')
    plt.plot(epochs2, train_accuracy_top52, marker='x', label='YOLOv8+attention')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy Top 5')
    plt.title('Top 5 Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.savefig('training_results_comparison.png')
    plt.show()


# Example usage
plot_training_results('/home/gth/PycharmProjects/Graduation_project/ML/runs/classify/train21/results.csv', '../train6/results.csv')
