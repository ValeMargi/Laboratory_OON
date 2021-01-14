from Lab010.core.Info.SignalInformation import SignalInformation
from Lab010.core.Elements.Network import Network
from Lab010.core.Elements.Connection import Connection

import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import statistics as st

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

    # Creating dataframe from csv file
    # df_ = pd.read_csv("../results/network_df.csv")
    network_fixed_rate.weighted_path = df

    # Create route space
    network_fixed_rate.update_routing_space(None)  # best_path = None => route space empty
    # print("Initial routing space for network with full switching matrices", network_with_full_switching_matrix.route_space)

    # Creating 100 connections with signal_power equal to 1 and with input/output nodes randomly chosen
    connections_fixed_rate = []
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
    connections_fixed_rate.append(Connection('F', 'A', 1e-3))
    connections_fixed_rate.append(Connection('D', 'A', 1e-3))
    connections_fixed_rate.append(Connection('A', 'B', 1e-3))
    connections_fixed_rate.append(Connection('F', 'E', 1e-3))
    connections_fixed_rate.append(Connection('A', 'D', 1e-3))
    connections_fixed_rate.append(Connection('B', 'D', 1e-3))
    connections_fixed_rate.append(Connection('A', 'D', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('A', 'E', 1e-3))
    connections_fixed_rate.append(Connection('A', 'C', 1e-3))
    connections_fixed_rate.append(Connection('D', 'F', 1e-3))
    connections_fixed_rate.append(Connection('A', 'D', 1e-3))
    connections_fixed_rate.append(Connection('F', 'D', 1e-3))
    connections_fixed_rate.append(Connection('F', 'A', 1e-3))
    connections_fixed_rate.append(Connection('D', 'F', 1e-3))
    connections_fixed_rate.append(Connection('C', 'F', 1e-3))
    connections_fixed_rate.append(Connection('D', 'B', 1e-3))
    connections_fixed_rate.append(Connection('C', 'D', 1e-3))
    connections_fixed_rate.append(Connection('D', 'E', 1e-3))
    connections_fixed_rate.append(Connection('E', 'A', 1e-3))
    connections_fixed_rate.append(Connection('A', 'D', 1e-3))
    connections_fixed_rate.append(Connection('E', 'B', 1e-3))
    connections_fixed_rate.append(Connection('F', 'E', 1e-3))
    connections_fixed_rate.append(Connection('B', 'F', 1e-3))
    connections_fixed_rate.append(Connection('E', 'A', 1e-3))
    connections_fixed_rate.append(Connection('A', 'E', 1e-3))
    connections_fixed_rate.append(Connection('A', 'E', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('C', 'A', 1e-3))
    connections_fixed_rate.append(Connection('B', 'E', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('A', 'B', 1e-3))
    connections_fixed_rate.append(Connection('D', 'A', 1e-3))
    connections_fixed_rate.append(Connection('A', 'F', 1e-3))
    connections_fixed_rate.append(Connection('E', 'B', 1e-3))
    connections_fixed_rate.append(Connection('C', 'A', 1e-3))
    connections_fixed_rate.append(Connection('C', 'F', 1e-3))
    connections_fixed_rate.append(Connection('D', 'B', 1e-3))
    connections_fixed_rate.append(Connection('E', 'F', 1e-3))
    connections_fixed_rate.append(Connection('A', 'D', 1e-3))
    connections_fixed_rate.append(Connection('D', 'E', 1e-3))
    connections_fixed_rate.append(Connection('A', 'C', 1e-3))
    connections_fixed_rate.append(Connection('E', 'B', 1e-3))
    connections_fixed_rate.append(Connection('A', 'B', 1e-3))
    connections_fixed_rate.append(Connection('E', 'D', 1e-3))
    connections_fixed_rate.append(Connection('F', 'D', 1e-3))
    connections_fixed_rate.append(Connection('A', 'F', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('C', 'B', 1e-3))
    connections_fixed_rate.append(Connection('F', 'E', 1e-3))
    connections_fixed_rate.append(Connection('D', 'E', 1e-3))
    connections_fixed_rate.append(Connection('B', 'A', 1e-3))
    connections_fixed_rate.append(Connection('F', 'E', 1e-3))
    connections_fixed_rate.append(Connection('D', 'A', 1e-3))
    connections_fixed_rate.append(Connection('F', 'C', 1e-3))
    connections_fixed_rate.append(Connection('D', 'B', 1e-3))
    connections_fixed_rate.append(Connection('C', 'E', 1e-3))
    connections_fixed_rate.append(Connection('C', 'B', 1e-3))
    connections_fixed_rate.append(Connection('F', 'C', 1e-3))
    connections_fixed_rate.append(Connection('C', 'A', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('A', 'C', 1e-3))
    connections_fixed_rate.append(Connection('B', 'E', 1e-3))
    connections_fixed_rate.append(Connection('E', 'A', 1e-3))
    connections_fixed_rate.append(Connection('F', 'D', 1e-3))
    connections_fixed_rate.append(Connection('C', 'A', 1e-3))
    connections_fixed_rate.append(Connection('D', 'B', 1e-3))
    connections_fixed_rate.append(Connection('A', 'E', 1e-3))
    connections_fixed_rate.append(Connection('E', 'B', 1e-3))
    connections_fixed_rate.append(Connection('C', 'D', 1e-3))
    connections_fixed_rate.append(Connection('D', 'E', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('E', 'F', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('A', 'B', 1e-3))
    connections_fixed_rate.append(Connection('A', 'E', 1e-3))
    connections_fixed_rate.append(Connection('F', 'D', 1e-3))
    connections_fixed_rate.append(Connection('C', 'A', 1e-3))
    connections_fixed_rate.append(Connection('E', 'B', 1e-3))
    connections_fixed_rate.append(Connection('C', 'A', 1e-3))
    connections_fixed_rate.append(Connection('F', 'C', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('B', 'A', 1e-3))
    connections_fixed_rate.append(Connection('D', 'B', 1e-3))
    connections_fixed_rate.append(Connection('A', 'F', 1e-3))
    connections_fixed_rate.append(Connection('E', 'C', 1e-3))
    connections_fixed_rate.append(Connection('E', 'B', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('A', 'F', 1e-3))
    connections_fixed_rate.append(Connection('B', 'D', 1e-3))
    connections_fixed_rate.append(Connection('D', 'C', 1e-3))
    connections_fixed_rate.append(Connection('A', 'E', 1e-3))
    connections_fixed_rate.append(Connection('B', 'F', 1e-3))

    # Saving 100 connections in a variable in order to create
    # a network with not full switching matrices considering the same connections
    connections_shannon = connections_fixed_rate[:]
    connections_flex_rate = connections_fixed_rate[:]

    print('Stream with label=snr')
    network_fixed_rate.stream(connections_fixed_rate, 'snr')

    # print('Printing route_space\n\n')
    # print(network.route_space)

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_fixed_rate if c.bit_rate != 0]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with Fixed rate')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Connections')
    plt.show()

    bit_rate_connections = [c.bit_rate for c in connections_fixed_rate if c.bit_rate != 0]
    plt.figure()
    plt.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - Fixed rate')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Connections')
    plt.show()
    print("Average bit rate for fixed rate", st.mean(bit_rate_connections))
    print("Total capacity", sum(bit_rate_connections))

    # Shannon
    network_shannon = Network('../resources/nodes_full_shannon.json')
    network_shannon.connect()
    network_shannon.weighted_path = df
    network_shannon.update_routing_space(None)  # Restore routing space

    print('Stream with label=snr')
    network_shannon.stream(connections_shannon, 'snr')

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_shannon]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with Shannon rate')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Connections')
    plt.show()
    bit_rate_connections = [c.bit_rate for c in connections_shannon if c.bit_rate!=0]
    plt.figure()
    plt.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - Shannon rate')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Connections')
    plt.show()
    print("Average bit rate for shannon rate", st.mean(bit_rate_connections))
    print("Total capacity", sum(bit_rate_connections))


    network_flex_rate = Network('../resources/nodes_full_flex_rate.json')
    network_flex_rate.connect()
    network_flex_rate.weighted_path = df
    network_flex_rate.update_routing_space(None)  # Restore routing space

    print('Stream with label=snr')
    network_flex_rate.stream(connections_flex_rate, 'snr')

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections_flex_rate]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with Flex rate')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Connections')
    plt.show()
    bit_rate_connections = [c.bit_rate for c in connections_flex_rate if c.bit_rate!=0]
    plt.figure()
    plt.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - Flex rate')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Connections')
    plt.show()
    print("Average bit rate for flex rate", st.mean(bit_rate_connections))
    print("Total capacity", sum(bit_rate_connections))

