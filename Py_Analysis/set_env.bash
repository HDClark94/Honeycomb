#!/bin/bash

_DIR=$(pwd)

MODULES='functions'

for module in $MODULES
do
	module_path=$_DIR/$module
	echo "adding module: $module_path"
	export PYTHONPATH=$module_path:$PYTHONPATH
done

#this is for tensor board
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:'/usr/local/cuda/extras/CUPTI/lib64'
