"""
copy all images into one folder ('../../dataset/images/all') because images are saved in multiple folders right now
"""

import os
import shutil


old_dir = '../../UAV-benchmark-M'
output_dir = '../../dataset/images/all'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


folder_names = os.listdir(old_dir)

for folder in folder_names:
    folder_path = old_dir + '/' + folder    # '../../UAV-benchmark-M/M0403'
    img_filename_ls = os.listdir(folder_path)    # 'img000061.jpg'

    for img_filename in img_filename_ls:
        # '../../UAV-benchmark-M/M0403/img000061.jpg'
        old_img_path = old_dir + '/' + folder + '/' + img_filename

        # ../../dataset/images/all/M0403_000061.jpg
        output_img_path = output_dir + '/' + folder + '_' + img_filename[-10:]

        # copy images from old path tp new path
        shutil.copyfile(old_img_path, output_img_path)

    print('image folder copy finished: ', folder)
print('all images has been copied into: ', output_dir)



