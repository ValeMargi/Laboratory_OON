from Lab07.core.Info.SignalInformation import SignalInformation
from Lab07.core.Elements.Network import Network
from Lab07.core.Elements.Connection import Connection

import pandas as pd
import json
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
import random as rand

if __name__ == '__main__':

    network_with_full_switching_matrix = Network('../resources/nodes_full.json')  # '../resources/nodes_full.json'
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

    # Creating dataframe from csv file
    # df_ = pd.read_csv("../results/network_df.csv")
    network_with_full_switching_matrix.weighted_path = df

    # Create route space
    network_with_full_switching_matrix.update_routing_space(None)  # best_path = None => route space empty
    # print("Initial routing space for network with full switching matrices", network_with_full_switching_matrix.route_space)

    # Creating 100 connections with signal_power equal to 1 and with input/output nodes randomly chosen
    connections_full = []
    nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections_full.append(Connection(input_rand, output_rand, 1e-3))
    # Saving 100 connections in a variable in order to create
    # a network with not full switching matrices considering the same connections
    connections_not_full = connections_full[:]

    pd.DataFrame(connections_full).to_csv(r'../results/connections_randomly.csv', index=False)
    print('Stream with label=snr')
    network_with_full_switching_matrix.stream(connections_full, 'snr')

    # print('Printing route_space\n\n')
    # print(network.route_space)

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_full]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with full switching matrices')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Connections')
    plt.show()

    ''' Printing the connections
        for i in range(0, 100):
            y = json.dumps(connections[i].__dict__)
            print(y)
    '''

    '''
    
    # Stream with label='latency'
    network.stream(connections)

    for i in range(0, 100):
        y = json.dumps(connections[i].__dict__)
        print(y)


    # plot the distribution of all the latencies
    latency_connections = [c.latency for c in connections]
    plt.figure()
    plt.hist(latency_connections, label='Latency distribution')
    plt.title('Latency distribution')
    plt.show()
    '''

    network_not_full = Network('../resources/nodes_not_full.json')
    network_not_full.connect()
    network_not_full.weighted_path = df
    network_not_full.update_routing_space(None)  # Restore routing space

    print('Stream with label=snr')
    network_not_full.stream(connections_not_full, 'snr')

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_not_full]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with not full switching matrices')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Connections')
    plt.show()
