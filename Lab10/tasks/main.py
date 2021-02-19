from Lab10.core.Info.SignalInformation import SignalInformation
from Lab10.core.Elements.Network import Network

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st

BIT_RATE_100G = 100e9
M = 8  # Full network saturatuion with fixed rate
# M=32 Full network saturatuion with shannon
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

    # Creating dataframe from csv file
    # df_ = pd.read_csv("../results/network_df.csv")
    network_fixed_rate.weighted_path = df

    # Create route space
    network_fixed_rate.update_routing_space(None)  # best_path = None => route space empty

    node_number = len(network_fixed_rate.nodes)
    traffic_matrix = {}
    #  Populate traffic matrix
    for node in network_fixed_rate.nodes.keys():
        traffic_matrix[node] = {}
        for node_ in network_fixed_rate.nodes.keys():
            if node != node_:
                traffic_matrix[node][node_] = BIT_RATE_100G * M

    completed_connections = node_number * node_number - node_number  # number of all possible connections
    connections = []
    # while there are still some possible connections to satisfy, the request_generation_traffic_matrix() method il call
    while completed_connections > 0:
        completed_connections -= network_fixed_rate.request_generation_traffic_matrix(traffic_matrix, connections,P_BASE)

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections if c.bit_rate != 0]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with Fixed rate')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Number of connections')
    plt.show()

    bit_rate_connections = [c.bit_rate for c in connections if c.bit_rate != 0]
    plt.figure()
    plt.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - Fixed rate')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Number of connections')
    plt.show()
    print("Average bit rate for fixed rate", st.mean(bit_rate_connections))
    print("Total capacity", sum(bit_rate_connections))

    network_flex = Network('../resources/nodes_full_flex_rate.json')
    network_flex.connect()
    network_flex.weighted_path = df
    network_flex.update_routing_space(None)  # Restore routing space

    node_number = len(network_flex.nodes)
    traffic_matrix = {}
    for node in network_flex.nodes.keys():
        traffic_matrix[node] = {}
        for node_ in network_flex.nodes.keys():
            if node != node_:
                traffic_matrix[node][node_] = BIT_RATE_100G * M

    completed_connections = node_number * node_number - node_number
    connections = []
    while completed_connections > 0:
        completed_connections -= network_flex.request_generation_traffic_matrix(traffic_matrix, connections, P_BASE)

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections if c.bit_rate != 0]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with Flex rate')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Number of connections')
    plt.show()

    bit_rate_connections = [c.bit_rate for c in connections if c.bit_rate != 0]
    plt.figure()
    plt.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - Flex rate')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Number of connections')
    # plt.xticks([0e11, 0.02e11, 0.04e11, 0.06e11, 0.08e11, 0.1e11])
    plt.show()
    print("Average bit rate for flex rate", st.mean(bit_rate_connections))
    print("Total capacity", sum(bit_rate_connections))

    # Shannon
    network_shannon = Network('../resources/nodes_full_shannon.json')
    network_shannon.connect()
    network_shannon.weighted_path = df
    network_shannon.update_routing_space(None)  # Restore routing space

    node_number = len(network_shannon.nodes)
    traffic_matrix = {}
    for node in network_shannon.nodes.keys():
        traffic_matrix[node] = {}
        for node_ in network_shannon.nodes.keys():
            if node != node_:
                traffic_matrix[node][node_] = BIT_RATE_100G * M

    completed_connections = node_number * node_number - node_number  # number of all possible connections
    connections = []
    while completed_connections > 0:
        completed_connections -= network_shannon.request_generation_traffic_matrix(traffic_matrix, connections, P_BASE)

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution with Shannon')
    plt.xlabel('SNR [dB]')
    plt.ylabel('Number of connections')
    plt.show()
    bit_rate_connections = [c.bit_rate for c in connections if c.bit_rate != 0]
    plt.figure()
    plt.hist(bit_rate_connections, label='Bit rate histogram')
    plt.title('Bit rate of accepted connections - Shannon')
    plt.xlabel('bit rate [bps]')
    plt.ylabel('Number of connections')
    plt.show()
    print("Average bit rate for shannon", st.mean(bit_rate_connections))
    print("Total capacity", sum(bit_rate_connections))


