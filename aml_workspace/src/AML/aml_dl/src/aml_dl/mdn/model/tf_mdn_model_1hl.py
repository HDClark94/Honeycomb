import tensorflow as tf
import math
import numpy as np
from aml_dl.utilities.tf_optimisers import optimiser_op

class MixtureDensityNetwork(object):

  def __init__(self, network_params, tf_sumry_wrtr=None):
    
    self._dim_input = network_params['dim_input']
    self._dim_output = network_params['dim_output']
    self._n_kernels = network_params['k_mixtures']
    self._n_hidden = network_params['n_hidden']
    self._optimiser = network_params['optimiser']
    self._dropout_prob = network_params['dropout_prob']
    self._tf_sumry_wrtr = tf_sumry_wrtr
    self._weight_multiplier = network_params['weight_multiplier']
    self._weight_reg_coef = network_params['weight_reg_coef']
    self._max_weight_mag = network_params['max_weight_mag']

  def _init_model(self, input_op = None):

    with tf.name_scope('input'):

      if input_op is None:
        self._x = tf.placeholder(dtype=tf.float32, shape=[None,self._dim_input],  name="x")
      else:
        self._x = input_op

      self._y = tf.placeholder(dtype=tf.float32, shape=[None,self._dim_output], name="y")

    with tf.name_scope('output_fc_op'):
      self._output_fc_op = self._init_fc_layer(self._x)[0]
      if self._tf_sumry_wrtr is not None:
        self._tf_sumry_wrtr.add_variable_summaries(self._output_fc_op)

    with tf.name_scope('init_mixture_params'):
      self._mus_op, self._sigmas_op, self._pis_op = self._init_mixture_parameters(self._output_fc_op)
      if self._tf_sumry_wrtr is not None:
        self._tf_sumry_wrtr.add_variable_summaries(self._mus_op)
        self._tf_sumry_wrtr.add_variable_summaries(self._sigmas_op)
        self._tf_sumry_wrtr.add_variable_summaries(self._pis_op)

    with tf.name_scope('cost_inv'):
      self._loss_op = self._init_loss(self._mus_op, self._sigmas_op, self._pis_op, self._y, self._init_fc_layer(self._x)[1], self._weight_reg_coef)
      if self._tf_sumry_wrtr is not None:
        self._tf_sumry_wrtr.add_variable_summaries(self._loss_op)

    
    self._train_op = self._init_train(self._loss_op)
    self._ops = {'x': self._x, 'y': self._y, 'mu': self._mus_op, 'sigma': self._sigmas_op, 'pi': self._pis_op, 'loss': self._loss_op, 'train': self._train_op}

    if self._tf_sumry_wrtr is not None:
      self._tf_sumry_wrtr.write_summary()

  def _init_fc_layer(self, input, stddev = 0.1):

    n_params_out = (self._dim_output + 2)*self._n_kernels
    # ---------edited 1156 300617--adds additional hidden layer

    Wh1 = tf.Variable(tf.random_normal([self._dim_input, self._n_hidden], stddev=stddev, dtype=tf.float32))
    bh1 = tf.Variable(tf.random_normal([1, self._n_hidden], stddev=stddev, dtype=tf.float32))
    
    Wo = tf.Variable(tf.random_normal([self._n_hidden, n_params_out], stddev=stddev, dtype=tf.float32))
    bo = tf.Variable(tf.random_normal([1, n_params_out], stddev=stddev, dtype=tf.float32))

    hidden_layer1 = tf.nn.tanh(tf.matmul(input, tf.multiply(tf.clip_by_norm(Wh1, self._max_weight_mag), self._weight_multiplier)) + bh1)
    hidden_layer1 = tf.nn.dropout(hidden_layer1, self._dropout_prob)
    output_fc = tf.matmul(hidden_layer1, tf.multiply(tf.clip_by_norm(Wo, self._max_weight_mag), self._weight_multiplier)) + bo

    # weightSum calculated for weight size regularization
    weightSquaredSum = tf.reduce_sum(tf.square(Wh1))  + tf.reduce_sum(tf.square(Wo)) + tf.reduce_sum(tf.square(bh1)) + tf.reduce_sum(tf.square(bo))
    #----------------------
    #tf.reduce_sum(Wh1,[0, 1]) + tf.reduce_sum(Wh2,[0, 1]) + tf.reduce_sum(Wh3,[0, 1]) + tf.reduce_sum(Wo,[0, 1]) +  + tf.reduce_sum(bh2) + tf.reduce_sum(bh3) + tf.reduce_sum(bo) tf.reduce_sum(bh1)
    return (output_fc, weightSquaredSum)

  def _init_mixture_parameters(self, output):

    c = self._dim_output
    m = self._n_kernels

    reshaped_output = tf.reshape(output,[-1, (c+2), m])
    mus = reshaped_output[:, :c, :]
    sigmas = tf.exp(reshaped_output[:, c, :])
    pis = tf.nn.softmax(reshaped_output[:, c+1, :])


    return mus, sigmas, pis


  def _init_loss(self, mus, sigmas, pis, ys, weightSum, weightCoef):

    m = self._n_kernels

    kernels = self._kernels(mus, sigmas, ys)

    result = tf.multiply(kernels,tf.reshape(pis, [-1, 1, m]))
    result = tf.reduce_sum(result, 2, keep_dims=True)

    epsilon = 1e-20
    result = -tf.log(tf.maximum(result,1e-20))

    return tf.reduce_mean(result, 0) + tf.multiply(tf.sqrt(weightSum), weightCoef)

  def _init_train(self,loss_op):

    train_op = optimiser_op(loss_op, self._optimiser)

    return train_op


  # Do the log trick here if it is not good enough the way it is now
  def _kernels(self, mus, sigmas, ys):
    c = self._dim_output
    m = self._n_kernels

    reshaped_ys = tf.reshape(ys, [-1, c, 1])
    reshaped_sigmas = tf.reshape(sigmas, [-1, 1, m])

    diffs = tf.subtract(mus, reshaped_ys) # broadcasting
    expoents = tf.reduce_sum( tf.multiply(diffs,diffs), 1, keep_dims=True )

    sigmacs = tf.pow(reshaped_sigmas,c)

    expoents = tf.multiply(-0.5,tf.multiply(tf.reciprocal(sigmacs), expoents))

    denominators = tf.pow(2*np.pi,c/2.0)*tf.sqrt(sigmacs)
    
    out = tf.div(tf.exp(expoents),denominators)

    return out

  def _mixture(self, kernels, pis):

    result = tf.multiply(kernels,tf.reshape(pis, [-1, 1, m]))
    mixture = tf.reduce_sum(result, 2, keep_dims=True)



  def run(self, sess, xs, ys = None):
    out = []
    if ys is None:
      out = sess.run([self._mus_op, self._sigmas_op, self._pis_op], feed_dict = { self._x: xs })
    else:
      out = sess.run([self._mus_op, self._sigmas_op, self._pis_op, self._loss_op], feed_dict = { self._x: xs, self._y: ys})

    return out

  def run_op(self, sess, op,  xs, ys = None):
    out = []

    if ys is None:
      out = sess.run([self._ops[op]], feed_dict = { self._x: xs })
    else:
      out = sess.run([self._ops[op]], feed_dict = { self._x: xs, self._y: ys })


    return out



class MixtureOfGaussians(object):


  def sample_pi_idx(self, x, pdf):
    N = pdf.size
    acc = 0

    for i in range(0, N):
      acc += pdf[i]
      if (acc >= x):
        return i

        print 'failed to sample mixture weight index'


    return -1


  def max_pi_idx(self, pdf):

    i = np.argmax(pdf)

    return i

  def sample_gaussian(self, rn, mu, std):


    return mu + rn*std

  def generate_mixture_samples_from_max_pi(self, out_pi, out_mu, out_sigma, m_samples=10):


    # Number of test inputs

    N = out_mu.shape[0]

    M = m_samples

    result = np.random.rand(N, M)
    rn  = np.random.randn(N, M) # normal random matrix (0.0, 1.0)

    # Generates M samples from the mixture for each test input

    for j in range(M):
      for i in range(0, N):
        idx = self.max_pi_idx(out_pi[i])
        mu = out_mu[i, idx]
        std = out_sigma[i, idx]
        result[i, j] = self.sample_gaussian(rn[i, j], mu, std)


    return result


  def generate_mixture_samples(self, out_pi, out_mu, out_sigma, m_samples=10):


    # Number of test inputs
    N = out_mu.shape[0]
    M = m_samples

    result = np.random.rand(N, M) # initially random [0, 1]
    rn  = np.random.randn(N, M) # normal random matrix (0.0, 1.0)
    mu  = 0
    std = 0
    idx = 0

    # Generates M samples from the mixture for each test input
    for j in range(M):
      for i in range(0, N):
        idx = self.sample_pi_idx(result[i, j], out_pi[i])
        mu = out_mu[i, idx]
        std = out_sigma[i, idx]
        result[i, j] = self.sample_gaussian(rn[i, j], mu, std)


    return result
