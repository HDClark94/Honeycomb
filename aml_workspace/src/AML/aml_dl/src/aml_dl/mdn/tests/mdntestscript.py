import os
import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from aml_dl.utilities.tf_batch_creator import BatchCreator
from aml_dl.mdn.model.mdn_push_fwd_model import MDNPushFwdModel
from aml_dl.mdn.utilities.get_data_from_files import get_data_from_files
from aml_dl.mdn.training.config_both_mdn_debug import network_params_fwd

