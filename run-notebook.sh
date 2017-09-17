#!/bin/bash
source activate lang-dec
exec jupyter notebook --ip=0.0.0.0 --port=5000 --no-browser --NotebookApp.token="langdec" >> /home/langdec/jupyter.log 
