#!/bin/bash

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
CONDA_DIR=$(pwd)/conda/
echo ${CONDA_DIR}
bash ./Miniconda3-latest-Linux-x86_64.sh -b -p ${CONDA_DIR}
rm -f ./Miniconda3-latest-Linux-x86_64.sh
export PATH="${CONDA_DIR}/bin:${PATH}"
conda install -y --file ./conda_requirements.txt
