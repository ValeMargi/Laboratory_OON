from Lab05.core.classes.Info.Lightpath import Lightpath
from Lab05.core.classes.Info.SignalInformation import SignalInformation

from Lab05.core.classes.Elements.Network import Line, Network
from Lab05.core.classes.Elements.Connection import Connection
from Lab05.core.classes.Elements.Node import Node

import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import random as rand

if __name__ == '__main__':

    network = Network('../resources/nodes.json')
    network.connect()
    node_labels = network.nodes.keys()
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
                for path in network.find_paths(pair[0], pair[1]):
                    path_string = ''
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[:-2])
                    # Propagation
                    '''l = Lightpath( 1, path, 0)
                    l = network.propagate(l)
                    latencies.append(l.latency)
                    noises.append(l.noise_power)
                    '''
                    signal_information = SignalInformation(1e-3, path)
                    signal_information = network.propagate(signal_information)
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
    network.draw()

    # Creating dataframe from csv file
    #df_ = pd.read_csv("../results/network_df.csv")
    network.weighted_path = df
    print('\nBest_highest_snr with path A -> B: \n', network.find_best_snr('A', 'B'))
    print('\nBest_highest_snr with path C -> D: \n', network.find_best_snr('C', 'D'))
    print('\nBest_lowest_latency with path A -> B: \n', network.find_best_latency('A', 'B'))
    print('\nBest_lowest_latency with path C -> D: \n', network.find_best_latency('C', 'D'))
    print('\nBest_lowest_latency with path E -> D: \n', network.find_best_latency('E', 'D'))
    

    connections = []
    nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections.append(Connection(input_rand, output_rand, 1e-3))

    
    print('*************************************************************')
    print('Test path A->B\n\n\n')
    test_connection = []
    test_connection.append(Connection('A', 'B', 1e-3))
    network.stream(test_connection, 'snr')
    print('Test_connection: \n\n ', test_connection)

    # Stream with label='snr'
    network.stream(connections, 'snr')

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution')
    plt.show()

    for i in range(0, 100):
        y = json.dumps(connections[i].__dict__)
        print(y)

    
    # Stream with label='latency'
    network.stream(connections)

    for i in range(0, 100):
        y = json.dumps(connections[i].__dict__)
        # print(y)

    
    # plot the distribution of all the latencies
    latency_connections = [c.latency for c in connections]
    plt.figure()
    plt.hist(latency_connections, label='Latency distribution')
    plt.title('Latency distribution')
    plt.show()
