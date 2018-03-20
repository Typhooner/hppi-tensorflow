from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, hppi

import tensorflow as tf
tf.logging.set_verbosity(tf.logging.INFO)

# Training Parameters
learning_rate = 0.01 # 0.01 => 0.001 => 0.0001
num_steps = 10000

# Network Parameters
num_input = 343 # HPPI data input
num_classes = 2 # HPPI total classes

def main():
  # Load datasets.
  hppids = hppi.read_data_sets(os.getcwd()+"/data/02-ct-bin", one_hot=False)

  # Specify that all features have real-value data
  feature_columns = [tf.feature_column.numeric_column("x", shape=[num_input])]

  # Build 3 layer DNN with 10, 20, 10 units respectively.
  classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                          # input_layer_partitioner=None,
                                          # hidden_units=[10, 20, 10],
                                          hidden_units=[256, 256, 256],
                                          # activation_fn=tf.nn.relu,
                                          n_classes=num_classes,
                                          # optimizer='Adagrad',
                                          optimizer=tf.train.AdamOptimizer(learning_rate=learning_rate),
                                          model_dir=os.getcwd()+"/model/train_with_tf_estimator_ct")
  # Define the training inputs
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.train.datas},
      y=hppids.train.labels,
      num_epochs=None,
      shuffle=True,
      queue_capacity=60000)

  # Train model.
  classifier.train(input_fn=train_input_fn, steps=num_steps)

  # Define the test inputs
  test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.test.datas},
      y=hppids.test.labels,
      num_epochs=1,
      shuffle=False)

  # Evaluate accuracy.
  accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

  print("\nTest Accuracy: {0:f}\n".format(accuracy_score))

if __name__ == "__main__":
    main()