import math

from matplotlib.offsetbox import AnchoredText

from Lab09.core.Elements.Network import Network
from Lab09.core.Elements.Connection import Connection
import random as rand
import matplotlib.pyplot as plt
import statistics as st
from matplotlib.widgets import TextBox

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
    net.stream(connections, 'snr')
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
    plt.title('SNR distribution with '+str(strategy)+' rate')
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
    print('Strategy = '+str(strategy)+' rate\n'+
          "Overall average bit rates of accepted connections: ", avg_bit_rate, 'Gbps\n'+
          "Total capacity allocated into the network: " , tot_capacity, 'Gbps')
    # text
    anchored_text = AnchoredText('Average bit rate = ' + str(avg_bit_rate)+'Gbps'+ '\nTotal capacity allocated = ' + str(tot_capacity)+'Gbps', loc='upper left', pad=0.5,prop=dict(size=9))
    ax.add_artist(anchored_text)
    plt.show()

