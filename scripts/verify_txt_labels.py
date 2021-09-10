"""
verify that if the generated txt labels are correct
"""

import cv2
import os
import random


images_dir = '../../dataset/images/all'
labels_dir = '../../dataset/labels/all'
ignore_dir = '../../UAV-benchmark-MOTD_v1.0/GT'

SHOW_IMGS = 50    # number of images to visualise
SHOW_IGNORE_AREA = False    # whether to show the ignore area
IMG_W = 1024
IMG_H = 540

img_name_ls = os.listdir(images_dir)
random.shuffle(img_name_ls)
txt_name_ls = os.listdir(labels_dir)

for img in img_name_ls:    # M0202_000196.jpg
    img_prefix = img[:12]    # M0202_000196
    SHOW_IMGS -= 1
    if SHOW_IMGS == 0:
        break

    for txt in txt_name_ls:    # M0202_000196.txt
        txt_prefix = txt[:12]    # M0202_000196

        if img_prefix == txt_prefix:
            img = cv2.imread(images_dir + '/' + img)
            txt_path = labels_dir + '/' + txt

            with open(txt_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    bbox = line.replace('\n', '').split(' ')    # [class_ind, xc, yc, w, h]
                    class_inx, xc, yc, w, h = bbox
                    x1 = float(xc) - float(w)/2
                    x2 = float(xc) + float(w)/2
                    y1 = float(yc) - float(h)/2
                    y2 = float(yc) + float(h)/2
                    x1 = int(x1 * IMG_W)
                    x2 = int(x2 * IMG_W)
                    y1 = int(y1 * IMG_H)
                    y2 = int(y2 * IMG_H)
                    img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), thickness=2)

                if SHOW_IGNORE_AREA:
                    video_num = img_prefix[:5]    # M0202
                    ignore_path = ignore_dir + '/' + video_num + '_gt_ignore.txt'    # '../../UAV-benchmark-MOTD_v1.0/GT/M0202_gt_ignore.txt'
                    img_num = img_prefix[-6:]    # 000196
                    with open(ignore_path, 'r') as ig_file:
                        ig_lines = ig_file.readlines()
                        for ig_line in ig_lines:
                            ig_line_ls = ig_line.split(',')    # ['1089', '20', '461', '207', '21', '31', '1', '1']
                            ig_img_num = ig_line_ls[0]    # '1089'
                            ig_img_num = (6 - len(ig_img_num)) * '0' + str(ig_img_num)    # '001089'

                            if str(ig_img_num) == str(img_num):
                                ig_x1 = int(ig_line_ls[2])
                                ig_y1 = int(ig_line_ls[3])
                                ig_x2 = int(ig_x1 + int(ig_line_ls[4])/2)
                                ig_y2 = int(ig_y1 + int(ig_line_ls[5])/2)
                                img = cv2.rectangle(img, (ig_x1, ig_y1), (ig_x2, ig_y2), (0, 255, 0), thickness=2)

                cv2.imshow('UAVDT', img)
                cv2.waitKey(0)






