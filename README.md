## 【0】Introduction

This repo is based on [YOLOv5 (5.0)](https://github.com/ultralytics/yolov5/releases/tag/v5.0) and aims at training the network with dataset [UA-DETRAC](https://detrac-db.rit.albany.edu/).

Running the repo in Colab is recommended, copy the file [YOLOv5_train_on_UA-DETRAC.ipynb](https://colab.research.google.com/drive/13zZ9W4_kIePyCS_TzJim0lytHaC850G3?usp=sharing), then run it on Colab. (remember to change the runtime type to GPU in Colab)



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
git clone https://github.com/forever208/yolov5_train_on_UA-DETRAC.git
```

Install all the python dependencies using pip:
```
cd yolov5_train_on_UA-DETRAC
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
- transform the label format and also save all txt label files into one folder .
- split dataset into training and validation set



### Copy all images into one folder
Using python script `yolov5_train_on_UAVDT/scripts/organise_image_folders.py` to do the job. 

```
cd yolov5_train_on_UAVDT/scripts/ 
python organise_image_folders.py
```

you should now get the following folder structure where `dataset/images/all` contains all 40k images
<p align="left">
  <img src="https://drive.google.com/drive/folders/1qHG9rM2UMU0BMPqrCaDfv6KHCBmMklmd?usp=sharing" width='25%' height='25%'/>
</p>



### Organize the dataset folder structure

run the following script to only pick up 1/10 images and rename images, move them into `/dataset/images/` 
```
python rename_image.py
```

only pick up 1/10 txts and rename them, move them into `/dataset/labels/` 
```
python rename_txt.py
```

You should now get the following folder structure: `/dataset`, it is parallel with `yolov5_train_on_UA-DETRAC`.  

(**this structure meets the demand of YOLOv5 custom training**)

<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UA-DETRAC/blob/master/data/images/folder_structure_2.png" width='25%' height='25%'/>
</p>


### Re-organize the training and validation set

For simplicity, I merely add the validation set into training set for the best training results.

Of course, you can train and val set togerther and do a random split (80% as training, 20% as validation).

```
# remove the redundant folder  
cd ../..
rm -rf DETRAC-Test-Annotations-XML/
rm -rf DETRAC-Train-Annotations-XML/
rm -rf Insight-MVT_Annotation_Test/
rm -rf Insight-MVT_Annotation_Train/
rm -rf test_detrac_txt/
rm -rf train_detrac_txt/

# add validation set into training set (because the distribution of DETRAC is biased in training set) 
cp -i -r ./dataset/images/val/. ./dataset/images/train/
cp -i -r ./dataset/labels/val/. ./dataset/labels/train/ 
```



## 【4】Train

### Configuration setting
Before training, you can modify some configurations according to you demand.

`yolov5_train_on_UA-DETRAC/data/UA_DETRAC.yaml` 

contains the image and label path for training, validation and testing. (we have well setted it up)

`yolov5_train_on_UA-DETRAC/model/yolov5m.yaml` 

contains the layers configuration and number of classes. (change the number of classes to 1)


### Train
Now, you can train the network with UA-DETRAC dataset.

Let's say, we use `YOLOv5m` as the pre-trained model to train `10 epochs` with the image size `640` in a single GPU

```
python train.py --img 640 --batch 16 --epochs 5 --data UA_DETRAC.yaml --weights yolov5m.pt 
```

For multi-GPUs training, let's say 4 GPUs, you can do:
```
python -m torch.distributed.launch --nproc_per_node 4 train.py --img 640 --batch 64 --epochs 10 --data UA_DETRAC.yaml --weights yolov5m.pt --device 0,1,2,3
```


Below is the all arguments you can tune for training:
<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UA-DETRAC/blob/master/data/images/training%20arguments.png" width='80%' height='80%'/>
</p>
