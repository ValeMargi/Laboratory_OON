import math

from matplotlib.offsetbox import AnchoredText

from Lab10.core.Elements.Network import Network
from Lab10.core.Elements.Connection import Connection
import random as rand
import matplotlib.pyplot as plt
import statistics as st
import pandas as pd
import numpy as np
import copy
from math import inf

BIT_RATE_100G = 100e9

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def network_initialization(path_nodes, weighted_path, connections):
    net = Network(path_nodes)
    net.connect()
    net.weighted_path = weighted_path
    net.update_routing_space(None)  # Restore routing space
    return net


def get_random_connections():
    connections_a = []
    nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections_a.append(Connection(input_rand, output_rand, 1e-3))
    return connections_a


def plot_snr_and_bit_rate(strategy, connections):
    snr_connections = [c.snr for c in connections]
    plt.figure()
    plt.hist(snr_connections, label='SNR distribution')
    plt.title('SNR distribution with ' + str(strategy) + ' rate')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Number of connections')
    plt.show()

    bit_rate_connections = [c.bit_rate for c in connections if c.bit_rate != 0]
    f, ax = plt.subplots(1, 1)
    ax.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - ' + str(strategy) + ' rate')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Number of connections')
    avg_bit_rate = truncate(st.mean(bit_rate_connections) / (1e9), 3)
    tot_capacity = truncate((sum(bit_rate_connections) / (1e9)), 3)
    print('Strategy = ' + str(strategy) + ' rate\n' +
          "Overall average bit rates of accepted connections: ", avg_bit_rate, 'Gbps\n' +
          "Total capacity allocated into the network: ", tot_capacity, 'Gbps')
    # text
    anchored_text = AnchoredText(
        'Average bit rate = ' + str(avg_bit_rate) + 'Gbps' + '\nTotal capacity allocated = ' + str(
            tot_capacity) + 'Gbps', loc='upper left', pad=0.5, prop=dict(size=9))
    ax.add_artist(anchored_text)
    plt.show()


def plot_traffic_matrix(traffic_matrix, strategy, M):
    a = pd.DataFrame.from_dict(traffic_matrix).to_numpy(dtype=float, na_value=None).astype(float)
    fig, ax = plt.subplots()

    for i in range(pd.DataFrame.from_dict(traffic_matrix).shape[0]):
        for j in range(pd.DataFrame.from_dict(traffic_matrix).shape[1]):
            text = ax.text(j, i, a[i, j],
                           ha="center", va="center", color="w")
    x_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    y_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    # Create dummy x values, with a value for every label entry
    x = np.r_[:len(x_labels)]
    y = np.r_[:len(y_labels)]
    # Change the xticks and yticks as desired
    plt.title('Traffic matrix with ' + str(strategy) + ' rate and M = ' + str(M))
    plt.xticks(x, x_labels)
    plt.yticks(y, y_labels)
    cmap = plt.cm.jet
    cmap = copy.copy(plt.cm.get_cmap("jet"))
    cmap.set_bad('orange', 1.)
    ax.imshow(a, interpolation='nearest', cmap=cmap)


def traffic_matrix_initialization(network, M):
    node_number = len(network.nodes)
    traffic_matrix = {}
    for node in network.nodes.keys():
        traffic_matrix[node] = {}
        for node_ in network.nodes.keys():
            if node != node_:
                traffic_matrix[node][node_] = BIT_RATE_100G * M
            else:
                traffic_matrix[node][node_] = inf
    return traffic_matrix
