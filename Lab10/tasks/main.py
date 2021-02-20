from Lab10.core.Info.SignalInformation import SignalInformation
from Lab10.core.Elements.Network import Network
from Lab10.core.utils import network_initialization, get_random_connections, plot_snr_and_bit_rate,plot_traffic_matrix, traffic_matrix_initialization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import copy
from math import inf

BIT_RATE_100G = 100e9
M = 8  # M=8 Full network saturatuion with fixed rate
#M=32   # M=32 Full network saturatuion with shannon
P_BASE = 1e-3

if __name__ == '__main__':

    network_fixed_rate = Network('../resources/nodes_full_fixed_rate.json')
    network_fixed_rate.connect()
    node_labels = network_fixed_rate.nodes.keys()
    pairs = []
    for label1 in node_labels:
        for label2 in node_labels:
            if label1 != label2:
                pairs.append(label1 + label2)
            columns = ['path', 'latency', 'noise', 'snr']
            df = pd.DataFrame()
            paths = []
            latencies = []
            noises = []
            snrs = []
            for pair in pairs:
                for path in network_fixed_rate.find_paths(pair[0], pair[1]):
                    path_string = ''
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[:-2])
                    signal_information = SignalInformation(P_BASE, path)
                    signal_information = network_fixed_rate.propagate(signal_information)
                    latencies.append(signal_information.latency)
                    noises.append(signal_information.noise_power)
                    snrs.append(10 * np.log10(1 / signal_information.isnr))
            df['path'] = paths
            df['latency'] = latencies
            df['noise'] = noises
            df['snr'] = snrs

    plt.figure()
    network_fixed_rate.draw()
    network_fixed_rate.weighted_path = df
    # Create route space
    network_fixed_rate.update_routing_space(None)  # best_path = None => route space empty

    #  Populate traffic matrix
    traffic_matrix = traffic_matrix_initialization(network_fixed_rate)
    node_number = len(network_fixed_rate.nodes)
    completed_connections = node_number * node_number - node_number  # number of all possible connections
    connections = []
    # while there are still some possible connections to satisfy, the request_generation_traffic_matrix() method il call
    while completed_connections > 0:
        completed_connections -= network_fixed_rate.request_generation_traffic_matrix(traffic_matrix, connections,P_BASE)
    # plot the distribution of all the snrs and bit rate
    plot_snr_and_bit_rate('Fixed', connections)
    # plot traffic matrix
    plot_traffic_matrix(traffic_matrix, 'Fixed', M)


    ''' Considering the flex-rate transceiver strategy '''
    # network_initialization() method calls the Network constructor, connect() method,
    # update_routing_space() method to restore the network
    network_flex_rate = network_initialization('../resources/nodes_full_flex_rate.json', df, connections)
    #  Populate traffic matrix
    traffic_matrix = traffic_matrix_initialization(network_flex_rate)
    node_number = len(network_flex_rate.nodes)
    completed_connections = node_number * node_number - node_number
    connections = []
    while completed_connections > 0:
        completed_connections -= network_flex_rate.request_generation_traffic_matrix(traffic_matrix, connections, P_BASE)
    # plot the distribution of all the snrs and bit rate
    plot_snr_and_bit_rate('Flex', connections)
    # plot traffic matrix
    plot_traffic_matrix(traffic_matrix, 'Flex', M)


    '''Considering the maximum theoretical Shannon rate'''
    # network_initialization() method calls the Network constructor, connect() method,
    # update_routing_space() method to restore the network '''
    network_shannon = network_initialization('../resources/nodes_full_shannon.json', df, connections)
    #  Populate traffic matrix
    traffic_matrix = traffic_matrix_initialization(network_shannon)
    node_number = len(network_shannon.nodes)
    completed_connections = node_number * node_number - node_number  # number of all possible connections
    connections = []
    while completed_connections > 0:
        completed_connections -= network_shannon.request_generation_traffic_matrix(traffic_matrix, connections, P_BASE)
    # plot the distribution of all the snrs and bit rate
    plot_snr_and_bit_rate('Shannon', connections)
    # plot traffic matrix
    plot_traffic_matrix(traffic_matrix, 'Shannon', M)
