#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/5/29 上午10:18
# @Author : Gao_Taiheng
# @File : plot.py
import pandas as pd
import matplotlib.pyplot as plt


def plot_training_results(csv_file):
    # Read CSV into a DataFrame
    df = pd.read_csv(csv_file)
    print(df.keys())

    # Extract data from DataFrame
    epochs = df['                  epoch']
    train_loss = df['             train/loss']
    train_accuracy_top1 = df['  metrics/accuracy_top1']
    train_accuracy_top5 = df['  metrics/accuracy_top5']
    val_loss = df['               val/loss']
    lr_pg0 = df['                 lr/pg0']
    lr_pg1 = df['                 lr/pg1']
    lr_pg2 = df['                 lr/pg2']

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.plot(epochs, train_loss, marker='o')
    plt.xlabel('Epoch')
    plt.ylabel('Train Loss')
    plt.title('Train Loss')

    plt.subplot(2, 2, 2)
    plt.plot(epochs, train_accuracy_top1, marker='o')
    plt.xlabel('epoch')
    plt.ylabel('metrics/accuracy_top1')
    plt.title('metrics/accuracy_top1')

    plt.subplot(2, 2, 3)
    plt.plot(epochs, val_loss, marker='o')
    plt.xlabel('epoch')
    plt.ylabel('val/loss')
    plt.title('Validation Loss')

    plt.subplot(2, 2, 4)
    plt.plot(epochs, lr_pg0, marker='o', label='pg0')
    plt.plot(epochs, lr_pg1, marker='o', label='pg1')
    plt.plot(epochs, lr_pg2, marker='o', label='pg2')
    plt.xlabel('Epoch')
    plt.ylabel('Learning Rate')
    plt.title('Learning Rate')
    plt.legend()

    plt.tight_layout()
    plt.savefig('training_results.png')
    plt.show()



# Example usage
plot_training_results('./results.csv')
