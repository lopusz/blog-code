#!/bin/bash
DIR=$(pwd)

CONDA_SHORT_DIR=$(dirname ${BASH_SOURCE[0]})/conda

cd ${CONDA_SHORT_DIR}
CONDA_BIN_DIR=$(pwd)/bin
cd ${DIR}

echo ${CONDA_BIN_DIR}

if echo $PATH | grep -qe "^${CONDA_BIN_DIR}:"; then
    echo "Python env already set-up"
else
    export PATH="${CONDA_BIN_DIR}:${PATH}"
    echo "Setting up python environment"
fi
