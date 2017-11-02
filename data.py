import pandas as pd
import tensorflow as tf
import numpy as np


def get_data(path, name):
    """
    path - str - relative path to data
    returns - tf.constant - the longitude (x axis) and latitude (y axis)
                            coordinates of all pickups and dropoffs in the
                            dataset
    """
    data = pd.read_csv(path,
                       parse_dates=['pickup_datetime',
                                    'dropoff_datetime'],
                       date_parser=pd.to_datetime)
    pickup_coordinates = data.loc[:, ['pickup_longitude',
                                      'pickup_latitude']].as_matrix()
    dropoff_coordinates = data.loc[:, ['dropoff_longitude',
                                       'dropoff_latitude']].as_matrix()
    coords = np.concatenate((pickup_coordinates, dropoff_coordinates))
    return tf.constant(coords, name=name, dtype=tf.float32)


def rotate(data, theta):
    """
    data - a 2-dimensional tensor of shape (?, 2)
    theta - the degree of rotation
    """
    rotation_matrix = tf.convert_to_tensor([[tf.cos(theta), -tf.sin(theta)],
                                            [tf.sin(theta), tf.cos(theta)]])
    return tf.matmul(rotation_matrix, data, transpose_b=True)


def bin_2d(dataset, num_bins, pad_longitude=.02, pad_latitude=.02):
        """
        dataset is a two dimensional numpy array of shape (?, 2)
        """
        xmin = np.min(dataset[:, 1]) - pad_longitude
        xmax = np.max(dataset[:, 1]) + pad_longitude
        ymin = np.min(dataset[:, 0]) - pad_latitude
        ymax = np.max(dataset[:, 0]) + pad_latitude
        H = np.histogram2d(dataset[:, 1],
                           dataset[:, 0],
                           bins=num_bins,
                           range=[[xmin, xmax], [ymin, ymax]])
        return H