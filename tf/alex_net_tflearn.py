#!/usr/bin/python
# -*- coding: utf-8 -*-

import tflearn
from tflearn.layers.core import input_data
from tflearn.layers.core import dropout
from tflearn.layers.core import fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

import tflearn.datasets.oxflower17 as oxflower17


if __name__ == "__main__":
    X, y = oxflower17.load_data(dirname="/home/buxizhizhoum/1-Work/Documents/2-Codes/machine_learning/tf/17flowers",
                                one_hot=True, resize_pics=(227, 227))

    network = input_data(shape=[None, 227, 227, 3])
    network = conv_2d(network, 96, 11, strides=4, activation="relu")
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = conv_2d(network, 256, 5, activation="relu")
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = conv_2d(network, 384, 3, activation="relu")
    network = max_pool_2d(network, 3, strides=2)
    network = local_response_normalization(network)

    network = fully_connected(network, 4096, activation="tanh")
    network = dropout(network, 0.5)
    network = fully_connected(network, 4096, activation="tanh")
    network = dropout(network, 0.5)
    network = fully_connected(network, 17, activation="softmax")
    network = regression(network,
                         optimizer="momentum",
                         loss="categorical_crossentropy",
                         learning_rate=0.001)

    # train
    model = tflearn.DNN(network,
                        checkpoint_path="model_alexnet",
                        max_checkpoints=1,
                        tensorboard_verbose=2)
    model.fit(X, y,
              n_epoch=1000,
              validation_set=0.1,
              shuffle=True,
              show_metric=True,
              batch_size=64,
              snapshot_step=200,
              snapshot_epoch=False,
              run_id="alexnet_oxflow17")

