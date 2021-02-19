from Lab05.core.Info.SignalInformation import SignalInformation
from Lab05.core.Elements.Network import Network
from Lab05.core.Elements.Connection import Connection

import pandas as pd
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

    # Create route space
    network.update_routing_space()

    connections = []
    nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections.append(Connection(input_rand, output_rand, 1e-3))

    #print('Stream with label=snr')
    network.stream(connections, 'snr')

    print('Printing route_space\n\n')
    print(network.route_space)

    # plot the distribution of all the snrs
    snr_connections = [c.snr for c in connections]
    plt.figure()
    plt.hist(snr_connections, label='Snr distribution')
    plt.title('SNR distribution')
    plt.ylabel('Number of connections')
    plt.xlabel('SNR [dB]')
    plt.show()

    '''for i in range(0, 100):
        y = json.dumps(connections[i].__dict__)
        print(y)
    '''

    network_latency = Network('../resources/nodes.json')
    network_latency.connect()
    network_latency.weighted_path = df
    network_latency.update_routing_space()

    print('Stream with label=snr')
    network_latency.stream(connections, 'snr')
    # Stream with label='latency'
    network.stream(connections)

    '''for i in range(0, 100):
        y = json.dumps(connections[i].__dict__)
        # print(y)
    '''

    # plot the distribution of all the latencies
    latency_connections = [c.latency*1e3 for c in connections]
    plt.figure()
    plt.hist(latency_connections, label='Latency distribution')
    plt.title('Latency distribution')
    plt.ylabel('Number of connections')
    plt.xlabel('Latency [ms]')
    plt.show()
