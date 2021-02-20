from Lab09.core.Info.SignalInformation import SignalInformation
from Lab09.core.Elements.Network import Network
from Lab09.core.Elements.Connection import Connection
from Lab09.core.utils import network_initialization, get_random_connections, plot_snr_and_bit_rate

import pandas as pd
import csv, copy
import numpy as np
import matplotlib.pyplot as plt
import random as rand

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

                    signal_information = SignalInformation(1e-3, path)
                    signal_information = network_fixed_rate.propagate(signal_information)
                    latencies.append(signal_information.latency)
                    noises.append(signal_information.noise_power)
                    snrs.append(
                        10 * np.log10(
                            signal_information.signal_power / signal_information.noise_power))
            df['path'] = paths
            df['latency'] = latencies
            df['noise'] = noises
            df['snr'] = snrs

    # Saving network dataframe without occupied channel into csv file
    # df.to_csv(r'../results/network_df.csv', index=False)

    plt.figure()
    network_fixed_rate.draw()
    network_fixed_rate.weighted_path = df

    # Create route space
    network_fixed_rate.update_routing_space(None)  # best_path = None => route space empty
    # print("Initial routing space for network with full switching matrices", network_with_full_switching_matrix.route_space)

    # Creating 100 connections with signal_power equal to 1 and with input/output nodes
    # randomly chosen and defined in 'connectionsFile.csv'
    connections_fixed_rate = []
    with open('../resources/connectionsFile.csv') as csv100ConnectionsFile:
        csvReader = csv.reader(csv100ConnectionsFile)
        for row in csvReader:
            connections_fixed_rate.append(Connection(row[0], row[1], float(row[2])))

    # Saving 100 connections in a variable in order to create
    # a network with not full switching matrices considering the same connections
    connections_shannon = copy.deepcopy(connections_fixed_rate[:])
    connections_flex_rate = copy.deepcopy(connections_fixed_rate[:])

    #print('Stream with label=snr')
    network_fixed_rate.stream(connections_fixed_rate, 'snr')

    # plot the distribution of all the snrs and bit rate
    plot_snr_and_bit_rate('Fixed', connections_fixed_rate)

    ''' Considering the flex-rate transceiver strategy '''

    # network_initialization() method calls the Network constructor, connect() method,
    # update_routing_space() method to restore the network and the stream() method with label='snr' '''
    network_flex_rate = network_initialization('../resources/nodes_full_flex_rate.json', df, connections_flex_rate)
    # plot the distribution of all the snrs and bit rate
    plot_snr_and_bit_rate('Flex', connections_flex_rate)

    '''Considering the maximum theoretical Shannon rate'''
    # network_initialization() method calls the Network constructor, connect() method,
    # update_routing_space() method to restore the network and the stream() method with label='snr' '''
    network_shannon = network_initialization('../resources/nodes_full_shannon.json', df, connections_shannon)

    # plot the distribution of all the snrs and bit rate
    plot_snr_and_bit_rate('Shannon', connections_shannon)

