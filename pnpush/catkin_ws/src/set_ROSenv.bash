#!/bin/bash

# file should be in appropriate root folder
ROS_DIR=$(pwd)

MODULES='pnpush_config pnpush_planning'

for module in $MODULES
do
	module_path=$ROS_DIR/$module/src/
	echo "adding module: $module_path"
	export PYTHONPATH=$module_path:$PYTHONPATH
done