#!/bin/bash

PROJECT_ROOT=/lang_dec

(source activate lang-dec || source /root/anaconda3/envs/lang-dec/bin/activate) && jupyter notebook --no-browser --ip=0.0.0.0 --allow-root $PROJECT_ROOT >> /var/log/lang-dec.log
