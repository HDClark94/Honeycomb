import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from aml_io.tf_io import load_tf_check_point
import time
from tf_mdn_model import MixtureDensityNetwork

class MDNPushFwdModel(object):

    def __init__(self, sess, network_params):

        self._sess = sess
        self._params = network_params
        self._device = self._params['device']
        self._tf_sumry_wrtr = None
        self._optimiser = network_params['optimiser']
        self._data_configured = False

        if network_params['write_summary']:
            if 'summary_dir' in network_params:
                summary_dir = network_params['summary_dir']
            else:
                summary_dir = None
            
            self._tf_sumry_wrtr = TfSummaryWriter(tf_session=sess,summary_dir=summary_dir)
            cuda_path = '/usr/local/cuda/extras/CUPTI/lib64'

            curr_ld_path = os.environ["LD_LIBRARY_PATH"]

            if not cuda_path in curr_ld_path.split(os.pathsep):
                print "Enviroment variable LD_LIBRARY_PATH does not contain %s"%cuda_path
                print "Please add it, else the program will crash!"
                raw_input("Press Ctrl+C")
                # os.environ["LD_LIBRARY_PATH"] = curr_ld_path + ':'+cuda_path

        with tf.device(self._device):

            self._mdn = MixtureDensityNetwork(network_params,
                                              tf_sumry_wrtr = self._tf_sumry_wrtr)
            self._mdn._init_model()
            self._net_ops = self._mdn._ops
            self._init_op = tf.global_variables_initializer()
            self._saver = tf.train.Saver()

    def init_model(self):

        with tf.device(self._device):
            self._sess.run(self._init_op)

            if self._params['load_saved_model']:
                self.load_model()


    #trains a network specified in self (prenormalized)
    def train_net(self, training_params):

        t0 = time.time()
        train_step = self._net_ops['train']
        loss_op  = self._net_ops['loss']

        epochs = training_params['epochs']
        val_step = training_params['val_step']
        stoch_samples = training_params['stoch_samples']
        minibatch = training_params['minibatch']
        train_x = training_params['train_x']
        train_y = training_params['train_y']
        val_x = training_params['val_x']
        val_y = training_params['val_y']

        with tf.device(self._device):
            self._sess.run(tf.global_variables_initializer())
        
            loss = np.zeros(epochs)
            val_loss = np.zeros(int(epochs)/val_step)
            val_counter = 0 
            #feed_dict, _ = self.get_data()

            for i in range(epochs):
                if (i%val_step == 0): #validation plus training
                    print "Starting epoch \t", i

                    #shuffle x and y in unison for minibatch permutations
                    train_x, train_y = shuffle(train_x, train_y)
                    
                    # counters scroll through dataset with width = minibatch
                    b_start_counter = 0 
                    b_end_counter = minibatch

                    # first minibatch
                    feed_dict = {self._net_ops['x']: train_x[0:minibatch], self._net_ops['y']: train_y[0:minibatch]}
                    feed_dict_val = {self._net_ops['x']: val_x[0:minibatch], self._net_ops['y']: val_y[0:minibatch]}
                    
                    # training loop
                    for j in range(int(len(train_x))/minibatch):
                        _, loss[i] = self._sess.run([train_step, loss_op], feed_dict=feed_dict)
            
                        b_start_counter += minibatch
                        b_end_counter += minibatch
                    
                        #shift minibatch on
                        feed_dict = {self._net_ops['x']: train_x[b_start_counter:b_end_counter], self._net_ops['y']: train_y[b_start_counter:b_end_counter]}
        
                    # calculate validation loss (with stochastic samples averages)
                    val_sum = 0
                    for j in range(int(len(val_x))):
                        stoch_sum = 0
                        feed_dict_val = {self._net_ops['x']: [val_x[j]], self._net_ops['y']: [val_y[j]]}
                        for l in range(stoch_samples):
                            stoch_sum += self._sess.run(loss_op, feed_dict=feed_dict_val)
                        val_sum += stoch_sum/stoch_samples
                    val_loss[val_counter] = val_sum/len(val_x)
                    val_counter += 1
                
                else: # just training
                    print "Starting epoch \t", i
                
                    #shuffle x and y in unison for minibatch permutations
                    train_x, train_y = shuffle(train_x, train_y)
                    
                    # counters scroll through dataset with width = minibatch
                    b_start_counter = 0 
                    b_end_counter = minibatch

                    # first minibatch
                    feed_dict = {self._net_ops['x']: train_x[0:minibatch], self._net_ops['y']: train_y[0:minibatch]}
                    feed_dict_val = {self._net_ops['x']: val_x[0:minibatch], self._net_ops['y']: val_y[0:minibatch]}
                    
                    # training loop
                    for j in range(int(len(train_x))/minibatch):
                        _, loss[i] = self._sess.run([train_step, loss_op], feed_dict=feed_dict)
            
                        b_start_counter += minibatch
                        b_end_counter += minibatch
                    
                        #shift minibatch on
                        feed_dict = {self._net_ops['x']: train_x[b_start_counter:b_end_counter], self._net_ops['y']: train_y[b_start_counter:b_end_counter]}
            
                # plotting updates
                if (i%val_step == 0) and (i>1):
                    plt.plot(range(0,i), loss[0:i], label = "loss")
                    plt.plot(range(0,i+1,val_step), val_loss[0:val_counter], label = "validation loss")
                    plt.xlabel('Epoch')
                    plt.ylabel('Error')
                    plt.legend()
                    plt.title(str(time.time()-t0/60) + ' minutes')
                    plt.show()

        return loss, val_loss


    def configure_data(self, data_x, data_y, batch_creator):
        self._data_x = data_x
        self._data_y = data_y
        self._batch_creator = batch_creator
        self._data_configured = True

    def get_model_path(self):
        if 'model_dir' in self._params:
            model_dir = self._params['model_dir']
        else:
            model_path = './fwd/'

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if 'model_name' in self._params:
            model_name = self._params['model_name']
        else:
            model_name = 'fwd_model.ckpt'

        return model_dir+model_name


    def load_model(self):
        load_tf_check_point(session=self._sess, filename=self.get_model_path())

    def save_model(self):
        save_path = self._saver.save(self._sess, self.get_model_path())
        print("Model saved in file: %s" % save_path)


    def get_data(self):
        round_complete = None 
        if self._params['batch_params'] is not None:
            if self._batch_creator is not None:
                self._data_x, self._data_y, round_complete = self._batch_creator.get_batch(random_samples=self._params['batch_params']['use_random_batches'])
            else:
                raise Exception("Batch training chosen but batch_creator not configured")

        if self._params['cnn_params'] is None:
            feed_dict = {self._net_ops['x']:self._data_x, self._net_ops['y']:self._data_y}
        else:
            feed_dict = {self._net_ops['image_input']:self._data_x, self._net_ops['y']:self._data_y}
        
        return feed_dict, round_complete

    def train(self, epochs):

        if not self._data_configured:
            raise Exception("Data not configured, please configure..")
        
        if self._params['write_summary']:
            tf.global_variables_initializer().run()
        
        loss = np.zeros(epochs)
        
        feed_dict, _ = self.get_data()

        if self._tf_sumry_wrtr is not None:

            for i in range(epochs):

                print "Starting epoch \t", i
                round_complete = False

                while not round_complete:

                    if self._params['batch_params'] is not None:
                        feed_dict, round_complete = self.get_data()
                    else:
                        #this is to take care of the case when we are not doing batch training.
                        round_complete = True

                    if round_complete:
                        print "Completed round"
    
                    if i % 100 == 99:  # Record execution stats
                        run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                        run_metadata = tf.RunMetadata()
                        summary, loss[i] = self._sess.run(fetches=[self._tf_sumry_wrtr._merged, self._net_ops['train_step']],
                                                    feed_dict=feed_dict,
                                                    options=run_options,
                                                    run_metadata=run_metadata)
                        
                        self._tf_sumry_wrtr.add_run_metadata(metadata=run_metadata, itr=i)
                        self._tf_sumry_wrtr.add_summary(summary=summary, itr=i)
                        print('Adding run metadata for', i)
                    else:  # Record a summary
                        summary, loss[i] = self._sess.run(fetches=[self._tf_sumry_wrtr._merged, self._net_ops['train_step']], 
                                                    feed_dict=feed_dict)
                        self._tf_sumry_wrtr.add_summary(summary=summary, itr=i)
           
            self._tf_sumry_wrtr.close_writer()

        else:
            with tf.device(self._device):
                # Keeping track of loss progress as we train
                train_step = self._net_ops['train']
                loss_op  = self._net_ops['cost']

                for i in range(epochs):
                  _, loss[i] = self._sess.run([train_step, loss_op], feed_dict=feed_dict)
  
        return loss

    def run_op(self, op_name, x_input):
        with tf.device(self._device):
            op = self._net_ops[op_name]

            out = self._sess.run(op, feed_dict={self._net_ops['x']: x_input})

            return out
