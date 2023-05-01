#!/bin/bash

SCRIPTS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BASE_DIR=${SCRIPTS_DIR%/*}

python3 ${BASE_DIR}/medusa/main.py ${BASE_DIR}