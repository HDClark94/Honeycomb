import os
from aml_robot.box2d.config import config
from aml_io.io_tools import get_aml_package_path

# training_data_dir = ''
# summary_dir       = os.environ['AML_DATA'] + '/aml_dl/mdn/summaries/'

# try:
#     training_data_dir = os.environ['AML_DATA'] + '/aml_dl/baxter_push_data/'
# except:
#     print "AML_DATA environment variable is not set."

# if not os.path.exists(training_data_dir):
#     print "Training data folder does not exist..."
#     #raise ValueError


NUM_FP         = 10 #this is not the right value?
IMAGE_WIDTH    = config['image_width']
IMAGE_HEIGHT   = config['image_height']
IMAGE_CHANNELS = 3


adam_params = {
    'type': 'adam',
    'params': {'learning_rate' : 0.001, 'beta1': 0.9, 'beta2': 0.999, 'epsilon': 1e-08, 'use_locking': False}
}

network_params_inv = {
    'dim_input': 14, 
    'dim_output': 2,
    'n_hidden': 24,
    'k_mixtures': 40,
    'batch_size': 25,
    'write_summary': True,
    'learning_rate': 0.0005,
    'image_width': IMAGE_WIDTH,
    'image_height': IMAGE_HEIGHT,
    'image_channels': IMAGE_CHANNELS,
    'image_size': IMAGE_WIDTH*IMAGE_HEIGHT*IMAGE_CHANNELS,
    'load_saved_model': False,
    'optimiser': adam_params,
    'device': '/cpu:0',
}