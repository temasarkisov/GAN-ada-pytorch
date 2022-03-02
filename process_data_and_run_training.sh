#!/bin/sh

#conda init zsh
#conda activate logan_torch_env

echo Enter images folder:
read IMAGES_FOLDER

python ../stylegan2-ada/image_proc.py --images_path=../stylegan2-ada/data/${IMAGES_FOLDER}
mv "../stylegan2-ada/data/${IMAGES_FOLDER}" "../stylegan2-ada/data/${IMAGES_FOLDER}_inverted"

python dataset_tool.py --source=../stylegan2-ada/data/${IMAGES_FOLDER}_inverted --dest=datasets/dataset_${IMAGES_FOLDER}_inverted.zip
#echo Enter GPUs indexes:
#read GPUS_INDEXES
#CUDA_VISIBLE_DEVICES=GPUS_INDEXES python train.py --data=datasets/dataset_thenounproject_rainbow_inverted.zip --outdir=training-runs/ --gpus=4 --snap=200



