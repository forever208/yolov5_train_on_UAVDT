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

## 【3】Download dataset

Download and unzip the dataset by command line is recommended:
```
cd ..
wget https://detrac-db.rit.albany.edu/Data/DETRAC-train-data.zip
wget https://detrac-db.rit.albany.edu/Data/DETRAC-test-data.zip
unzip DETRAC-train-data.zip
unzip DETRAC-test-data.zip
rm -rf DETRAC-test-data.zip
rm -rf DETRAC-train-data.zip
```

Then download and unzip the annotation files (I saved the file in my GoogleDrive), download by command:
```
wget wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1f-4NA2sc6Tqo25Ilx-b5NaFGLjhf2AbK' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1f-4NA2sc6Tqo25Ilx-b5NaFGLjhf2AbK" -O DETRAC-Train-Annotations-XML.zip && rm -rf /tmp/cookies.txt

wget wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1Q0E-Dk3vL55m9ODOENeq2_ojiZwWMbdo' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1Q0E-Dk3vL55m9ODOENeq2_ojiZwWMbdo" -O DETRAC-Test-Annotations-XML.zip && rm -rf /tmp/cookies.txt

unzip DETRAC-Train-Annotations-XML.zip
unzip DETRAC-Test-Annotations-XML.zip
rm -rf DETRAC-Train-Annotations-XML.zip
rm -rf DETRAC-Test-Annotations-XML.zip
```

## 【3】Dataset preprocessing
We then need to do 3 things before training YOLOv5 using UA-DERTAC dataset:
- transform the annotation format from xml to txt (the label format of YOLOv5 is txt).
- organize the dataset folder structure to meet the requirment of YOLOv5 default setting.
- re-organize the training set and validation set because the original split of DETRAC is not good (refer to [this blog](https://zhuanlan.zhihu.com/p/373096271) for more details)



### Transform xml to txt
Using python script `yolov5_train_on_UA-DETRAC/scripts/bigxml_txt.py` to do the transformation. 

```
cd yolov5_train_on_UA-DETRAC/scripts/ 
python bigxml_txt.py
```

you should now get the following folder structure where `train_detrac_txt` and `test_detrac_txt` are the txt labels.
<p align="left">
  <img src="https://github.com/forever208/yolov5_train_on_UA-DETRAC/blob/master/data/images/folder_structure_1.png" width='25%' height='25%'/>
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
