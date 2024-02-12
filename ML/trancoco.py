#!/usr/bin/env python
# -- coding: utf-8 --
# @Time : 2024/1/2 下午7:31
# @Author : Gao_Taiheng
# @File : trancoco.py
import os


def write_txt_file(file_path, file_list):
    with open(file_path, 'w') as file:
        for item in file_list:
            file.write(item + "\n")


def process_dataset(dataset_path, labels_path, split_type):
    txt_file_path = os.path.join(dataset_path, f"{split_type}.txt")

    with open(txt_file_path, 'w') as txt_file:
        for class_name in os.listdir(os.path.join(dataset_path, split_type)):
            pic_dir = os.path.join(dataset_path, split_type, class_name)
            for pic in os.listdir(pic_dir):
                txt_file.write(pic + "\n")

                label_file_path = os.path.join(labels_path, f"{pic.split('.')[0]}.txt")
                with open(label_file_path, 'w') as label_file:
                    label_file.write(class_name + "\n")


if __name__ == "__main__":
    dataset_path = "./data/archive/image/Dataset/"
    labels_path = "./data/labels/"

    # 处理训练集
    process_dataset(dataset_path, labels_path, "train")

    # 处理验证集
    process_dataset(dataset_path, labels_path, "valid")

# list_dir = os.listdir(path)
# for name_dir in list_dir:
#     if "new" in name_dir or "New" in name_dir:
#         list_dir_child = os.listdir(path + name_dir)
#         path_child = path + name_dir + "/" + list_dir_child[0] + "/"
#         print(path_child)
#         # os.mkdir(path_child + "train.txt") # 要写入图片
#         with open(path_child + "train.txt", 'w') as all_picture:
#             # open dir and read dir list , write in train.txt
#             for class_name in os.listdir(path_child + "train"):
#                 for picture_name in os.listdir(path_child + "train/" + class_name):
#                     all_picture.write(picture_name + '\n')
#                     with open("/home/gth/PycharmProjects/Graduation_project/ML/data/labels/" + picture_name.split('.')[0] + ".txt", 'w') as label:
#                         label.write(class_name)
#
#         with open(path_child + "val.txt", 'w') as all_picture:
#             # open dir and read dir list , write in val.txt
#             for class_name in os.listdir(path_child + "valid"):
#                 print(path_child + "valid/")
#                 for picture_name in os.listdir(path_child + "valid/" + class_name):
#                     all_picture.write(picture_name + '\n')
#                     with open("/home/gth/PycharmProjects/Graduation_project/ML/data/labels/" + picture_name.split('.')[
#                         0] + ".txt", 'w') as label:
#                         label.write(class_name)
