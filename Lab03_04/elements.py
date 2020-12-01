import pandas as pd
from scipy.constants import c
from Lab03_04.info import SignalInformation
import json
import numpy as np
import matplotlib.pyplot as plt
import random as rand


class Node(object):
    def __init__(self, node_dict):
        self._label = node_dict['label']
        self._position = node_dict['position']
        self._connected_nodes = node_dict['connected_nodes']
        self._successive = {}  # empty dic [line]

    # avoid any change in attributes -> private elements
    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def propagate(self, signal_information):
        path = signal_information.path
        if len(path) > 1:
            line_label = path[:2]  # 2 first elements of path
            line = self.successive[line_label]
            signal_information.next()
            signal_information = line.propagate(signal_information)
        return signal_information


class Line(object):
    def __init__(self, line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._successive = {}
        self._state = 'free'

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = 1e-3 * signal_power * self.length
        return noise

    def propagate(self, signal_information):
        # Update latency
        latency = self.latency_generation()
        signal_information.add_latency(latency)

        # Update noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)

        node = self.successive[signal_information.path[0]]
        signal_information = node.propagate(signal_information)
        return signal_information


class Network(object):
    def __init__(self, json_path):
        node_json = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}
        self._weighted_path = pd.DataFrame()

        # node_label = key
        for node_label in node_json:
            # Create the node instance
            node_dict = node_json[node_label]
            node_dict['label'] = node_label
            node = Node(node_dict)
            self._nodes[node_label] = node
            # Create the line instances
            for connected_node_label in node_dict['connected_nodes']:
                line_dict = {}
                line_label = node_label + connected_node_label
                line_dict['label'] = line_label
                node_position = np.array(node_json[node_label]['position'])
                connected_node_position = np.array(node_json[connected_node_label]['position'])
                line_dict['length'] = np.sqrt(
                    np.sum((node_position - connected_node_position) ** 2)
                )
                line = Line(line_dict)
                self._lines[line_label] = line

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def weighted_path(self):
        return self._weighted_path

    @weighted_path.setter
    def weighted_path(self, weighted_path):
        self._weighted_path = weighted_path

    def draw(self):
        nodes = self.nodes
        for node_label in nodes:
            n0 = nodes[node_label]
            x0 = n0.position[0]
            y0 = n0.position[1]
            plt.plot(x0, y0, 'go', markersize=10)
            plt.text(x0 + 20, y0 + 20, node_label)
            for connected_node_label in n0.connected_nodes:
                n1 = nodes[connected_node_label]
                x1 = n1.position[0]
                y1 = n1.position[1]
                plt.plot([x0, x1], [y0, y1], 'b')
        plt.title('Network')
        plt.show()

    def find_paths(self, label1, label2):
        cross_nodes = [key for key in self.nodes.keys()
                       if ((key != label1) & (key != label2))]
        cross_lines = self.lines.keys()
        inner_paths = {'0': label1}
        for i in range(len(cross_nodes) + 1):
            inner_paths[str(i + 1)] = []
            for inner_path in inner_paths[str(i)]:
                inner_paths[str(i + 1)] += [inner_path + cross_node for cross_node in cross_nodes
                                            if ((inner_path[-1] + cross_node in cross_lines) & (
                                cross_node not in inner_path))]
        paths = []
        for i in range(len(cross_nodes) + 1):
            for path in inner_paths[str(i)]:
                if path[-1] + label2 in cross_lines:
                    paths.append(path + label2)
        return paths

    def connect(self):
        nodes_dict = self.nodes
        lines_dict = self.lines

        for node_label in nodes_dict:
            node = nodes_dict[node_label]
            for connected_node in node.connected_nodes:
                line_label = node_label + connected_node
                line = lines_dict[line_label]
                line.successive[connected_node] = nodes_dict[connected_node]
                node.successive[line_label] = lines_dict[line_label]

    def propagate(self, signal_information):
        path = signal_information.path
        start_node = self.nodes[path[0]]
        propagated_signal_information = start_node.propagate(signal_information)
        return propagated_signal_information

    # Lab4
    def find_best_snr(self, node_input, node_output):
        if (node_input != node_output):
            my_df = network.weighted_path
            my_df.sort_values(by=['snr'], inplace=True, ascending=False)
            my_df_filtered = my_df[(my_df['path'].str[0] == node_input) & (my_df['path'].str[-1] == node_output)]
            found = False
            for i in my_df_filtered.values:
                path = i[0]  # path
                node1 = path[0]
                free_flag = True
                for node_i in range(3, len(path), 3):
                    line = self.lines[node1 + path[node_i]]
                    if line.state != 'free':
                        free_flag = False
                        break
                    node1 = path[node_i]
                if free_flag == True:
                    found = True
                    break
            if found == True:
                return i, i[0]
            else:
                return None, None
        else:
            return None, None

    def find_best_latency(self, node_input, node_output):
        if (node_input != node_output):
            my_df = network.weighted_path
            my_df.sort_values(by=['latency'], inplace=True, ascending=True)
            my_df_filtered = my_df[(my_df['path'].str[0] == node_input) & (my_df['path'].str[-1] == node_output)]
            found = False
            for i in my_df_filtered.values:
                path = i[0]
                node1 = path[0]
                free_flag = True
                for node_i in range(3, len(path), 3):
                    line = self.lines[node1 + path[node_i]]
                    if line.state != 'free':
                        free_flag = False
                        break
                    node1 = path[node_i]
                if free_flag == True:
                    found = True
                    break
            if found == True:
                return i, i[0]
            else:
                return None, None
        else:
            return None, None

    def stream(self, connections, label='latency'):
        for connection in connections:
            if label == 'snr':
                best_path_array, best_path = self.find_best_snr(connection.input, connection.output)
            else:
                best_path_array, best_path = self.find_best_latency(connection.input, connection.output)

            if best_path is not None:
                path_label = ''
                for index in range(0, len(best_path), 3):
                    path_label += best_path[index]
                si = SignalInformation(connection.signal_power, path_label)
                self.propagate(si)
                self.set_line_status(best_path)
                connection.snr = self.snr_dB(1e-3 * si.signal_power, si.noise_power)
                connection.latency = si.latency
            else:
                connection.snr = 0
                connection.latency = None

    def snr_dB(self, signal_power, noise_power):
        return 10 * np.log10(signal_power / noise_power)

    def set_line_status(self, current_path):
        node1 = current_path[0]
        for node_i in current_path[3:len(current_path):3]:
            line = self.lines[node1 + node_i]
            line.state = 'occupied'
            node1 = node_i

class Connection(object):
    def __init__(self, input, output, signal_power):
        self._input = input
        self._output = output
        self._signal_power = signal_power
        self._latency = 0.00
        self._snr = 0.00

    def __repr__(self):
        return "<Connection input:%s  output:%s signal_power:%d latency:%r snr:%f>" % (
        self.input, self.output, self.signal_power, self.latency, self.snr)

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @property
    def snr(self):
        return self._snr

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @snr.setter
    def snr(self, snr):
        self._snr = snr


if __name__ == '__main__':
    network = Network('nodes.json')
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
                    signal_information = SignalInformation(1, path)
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

    network.draw()

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
        connections.append(Connection(input_rand, output_rand, 1.00))
        
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
        #print(y)

    # Stream with label='latency'
    network.stream(connections)

    for i in range(0, 100):
        y = json.dumps(connections[i].__dict__)
        # print(y)

    # plot the distribution of all the latencies
    '''latency_connections = [c.latency for c in connections]
    plt.figure()
    plt.hist(latency_connections, label='Latency distribution')
    plt.title('Latency distribution')
    plt.show()
    '''

    '''print('Test path A->B\n\n\n')
    test_connection = []
    test_connection.append(Connection('A', 'B', 1))
    network.stream(test_connection, 'snr')
    print('Test_connection: \n\n ', test_connection)'''

