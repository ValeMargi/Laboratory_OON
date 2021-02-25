from Lab07.core.Info.SignalInformation import SignalInformation
from Lab07.core.Elements.Network import Network
from Lab07.core.Elements.Connection import Connection

import pandas as pd
import csv, copy
import numpy as np
import matplotlib.pyplot as plt
import random as rand

if __name__ == '__main__':

    ''' Network with all full switching matrices, so the lightpath can travel
     from and to any line connected to the node except going backwards on the same line'''
    network_with_full_switching_matrix = Network('../resources/nodes_full.json')
    network_with_full_switching_matrix.connect()
    node_labels = network_with_full_switching_matrix.nodes.keys()
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
                for path in network_with_full_switching_matrix.find_paths(pair[0], pair[1]):
                    path_string = ''
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[:-2])

                    signal_information = SignalInformation(1e-3, path)
                    signal_information = network_with_full_switching_matrix.propagate(signal_information)
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
    network_with_full_switching_matrix.draw()
    network_with_full_switching_matrix.weighted_path = df

    # Create route space
    network_with_full_switching_matrix.update_routing_space(None)  # best_path = None => route space empty

    # Creating 100 connections with signal_power equal to 1 and with input/output nodes randomly chosen
    connections_full = []
    '''
    nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections_full.append(Connection(input_rand, output_rand, 1e-3))
    '''
    with open('../resources/connectionsFile.csv') as csv100ConnectionsFile:
        csvReader = csv.reader(csv100ConnectionsFile)
        for row in csvReader:
            connections_full.append(Connection(row[0], row[1], float(row[2])))

    # Saving 100 connections in a variable in order to create
    # a network with not full switching matrices considering the same connections
    connections_not_full = copy.deepcopy(connections_full[:])
    print("Full switching matrix")
    network_with_full_switching_matrix.stream(connections_full, 'snr')

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_full]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with full switching matrices')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Number of connections')
    plt.show()


    ''' Network with not full switching matrices'''
    network_not_full = Network('../resources/nodes_not_full.json')
    network_not_full.connect()
    network_not_full.weighted_path = df
    network_not_full.update_routing_space(None)  # Restore routing space
    print("Not Full switching matrix")
    network_not_full.stream(connections_not_full, 'snr')

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_not_full]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with not full switching matrices')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Number of connections')
    plt.show()

