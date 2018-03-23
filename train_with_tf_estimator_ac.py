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
num_input = 420 # HPPI data input
num_classes = 2 # HPPI total classes

cwd = os.getcwd()
data_sets_dir = cwd+"/data/03-ac-bin"
model_dir = cwd+"/model/train_with_tf_estimator_ac"
result_file = cwd+"/model/result_of_tf_estimator_ac_256x256x256_relu_adam"+"_{0:g}".format(learning_rate)+".txt"

times = 1

def main():
  # Load datasets.
  hppids = hppi.read_data_sets(data_sets_dir, one_hot=False)

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
                                          model_dir=model_dir)
  # Define the training inputs
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.train.datas},
      y=hppids.train.labels,
      num_epochs=None,
      shuffle=True,
      queue_capacity=hppids.train.length)

  # Train model.
  classifier.train(input_fn=train_input_fn, steps=num_steps)

  # Define the test inputs
  test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": hppids.test.datas},
      y=hppids.test.labels,
      num_epochs=1,
      shuffle=False)

  # Evaluate accuracy.
  #accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
  # Evaluate scores.
  scores = classifier.evaluate(input_fn=test_input_fn)
  scores_str =   "global_step = {0:08d}".format(scores["global_step"]) \
             + ", accuracy = {0:8g}".format(scores["accuracy"]) \
             + ", accuracy_baseline = {0:8g}".format(scores["accuracy_baseline"]) \
             + ", auc = {0:8g}".format(scores["auc"]) \
             + ", auc_precision_recall = {0:8g}".format(scores["auc_precision_recall"]) \
             + ", average_loss = {0:8g}".format(scores["average_loss"]) \
             + ", label/mean = {0:8g}".format(scores["label/mean"]) \
             + ", loss = {0:8g}".format(scores["loss"]) \
             + ", prediction/mean = {0:8g}".format(scores["prediction/mean"]) \

  #print("\nTest Accuracy: {0:f}\n".format(accuracy_score))
  print("\nTest scores: {0}\n".format(scores_str))

  with open(result_file, "a") as file:
    file.write(scores_str+"\n")

if __name__ == "__main__":
  for _ in range(times):
    main()
