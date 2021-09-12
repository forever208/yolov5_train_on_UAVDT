## 【0】Introduction

This repo is based on [YOLOv5 (5.0)](https://github.com/ultralytics/yolov5/releases/tag/v5.0) and aims at training the network with dataset [UAVDT](https://sites.google.com/view/grli-uavdt/%E9%A6%96%E9%A1%B5).

Running the repo in Colab is recommended, copy the file [YOLOv5_train_on_UAVDT.ipynb](https://colab.research.google.com/drive/1Gq3HCV6AlEbAkQ-S3_l4-PRHpnbyfisF?usp=sharing), then run it on Colab. (remember to change the runtime type to GPU in Colab)



## 【1】Environment (Colab user can skip this step) 

* Python >=3.7
* Pytorch >=1.7

Create a new conda called YOLOv5, install pytorch-1.7.0
```
conda create --name YOLOv5 python=3.7
conda activate YOLOv5

# for GPU and CUDA 10.2
conda install pytorch==1.7.0 torchvision==0.8.0 torchaudio==0.7.0 cudatoolkit=10.2 -c pytorch
```


## 【2】Installation

Clone the code
```
git clone https://github.com/forever208/yolov5_train_on_UAVDT.git
```

Install all the python dependencies using pip:
```
cd yolov5_train_on_UAVDT
pip install -qr requirements.txt
```


## 【3】Download dataset - UAVDT

Download and unzip the dataset by command line is recommended:
```
cd ..
wget wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1m8KA6oPIRK_Iwt9TYFquC87vBc_8wRVc' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1m8KA6oPIRK_Iwt9TYFquC87vBc_8wRVc" -O UAVDTM.zip && rm -rf /tmp/cookies.txt

unzip UAVDTM.zip
rm -rf UAVDTM.zip
```

Then download and annotation file by command:
```
wget wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=19498uJd7T9w4quwnQEy62nibt3uyT9pq' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=19498uJd7T9w4quwnQEy62nibt3uyT9pq" -O UAV-benchmark-MOTD_v1.0.zip && rm -rf /tmp/cookies.txt

unzip UAV-benchmark-MOTD_v1.0.zip
rm -rf UAV-benchmark-MOTD_v1.0.zip
```


## 【3】Dataset preprocessing
We then need to do 3 things before training YOLOv5 using UAVDT dataset:
- copy all images into one folder since the original images are saved in multiple folders.
- transform the label format and also save all txt label files into one folder.
- split dataset into training and validation set



### Copy all images into one folder
Using python script `yolov5_train_on_UAVDT/scripts/organise_image_folders.py` to do the job. 

```
cd yolov5_train_on_UAVDT/scripts/ 
python organise_image_folders.py
```

you should now get the following folder structure where `dataset/images/all` contains all 40k images
<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UAVDT/blob/master/data/images/image%20folder.png" width='25%' height='25%'/>
</p>



### Transform the label format

Running the below script to match each image with a txt label file, move txts into `/dataset/labels/all` 
```
python organise_txt_labels.py
```

the label format is shown as follows, each line of txt is a ground truth bounfing box with format `class_index, x_center, y_center, width, height`
<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UAVDT/blob/master/data/images/label%20format.png" width='40%' height='40%'/>
</p>




### Split dataset into training and validation

I use 35k images as the training dataset, 5k images as the validation set

```
python split_train_val.py
```

You should now get the following folder structure: `/dataset`, it is parallel with `yolov5_train_on_UAVDT`.  

(**this structure meets the demand of YOLOv5 custom training**)

<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UA-DETRAC/blob/master/data/images/folder_structure_2.png" width='25%' height='25%'/>
</p>


To remove the redundant folders:

```
cd ../..
rm -rf UAV-benchmark-M
rm -rf UAV-benchmark-MOTD_v1.0
```

For best training results, you can also use all 40k images as the training dataset, run the command:

```
cp -i -r ./dataset/images/val/. ./dataset/images/train/
cp -i -r ./dataset/labels/val/. ./dataset/labels/train/ 
```


## 【4】Train

### Configuration setting
Before training, you can modify some configurations according to you demand.

`yolov5_train_on_UAVDT/data/UAVDT.yaml` 
contains the image and label path for training, validation and testing. (we have well setted it up)


`yolov5_train_on_UAVDT/model/yolov5m.yaml` 
contains the layers configuration and number of classes. (change the number of classes to 1)


### Train
Now, you can train the network with UAVDT dataset.

Let's say, we use `YOLOv5m` as the pre-trained model to train `10 epochs` with the image size `640` in a single GPU

```
python train.py --img 640 --batch 16 --epochs 5 --data UAVDT.yaml --weights yolov5m.pt 
```

For multi-GPUs training, let's say 4 GPUs, you can do:
```
python -m torch.distributed.launch --nproc_per_node 4 train.py --img 640 --batch 64 --epochs 10 --data UAVDT.yaml --weights yolov5m.pt --device 0,1,2,3
```


Below is the all arguments you can tune for training:
<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UA-DETRAC/blob/master/data/images/training%20arguments.png" width='80%' height='80%'/>
</p>
