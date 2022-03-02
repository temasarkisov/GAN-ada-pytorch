#!/bin/sh

echo Enter model path:
read MODEL_PATH

echo Enter slug to save:
read SLUG

python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=${MODEL_PATH} --output_dir=outputs/output_${SLUG}_0_3 --trunc=0.3
python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=${MODEL_PATH} --output_dir=outputs/output_${SLUG}_0_5 --trunc=0.5
python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=${MODEL_PATH} --output_dir=outputs/output_${SLUG}_0_7 --trunc=0.7
python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=${MODEL_PATH} --output_dir=outputs/output_${SLUG}_1_0 --trunc=1

