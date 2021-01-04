import pandas as pd
from Lab07.core.Elements.Node import Node
from Lab07.core.Elements.Line import Line
from Lab07.core.Info.Lightpath import Lightpath
import json
import numpy as np
import matplotlib.pyplot as plt


class Network(object):
    def __init__(self, json_path):
        node_json = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}
        self._weighted_path = pd.DataFrame()
        self._route_space = pd.DataFrame()

        self._switching_matrix = {}

        paths = []
        channel_0 = []
        channel_1 = []
        channel_2 = []
        channel_3 = []
        channel_4 = []
        channel_5 = []
        channel_6 = []
        channel_7 = []
        channel_8 = []
        channel_9 = []
        self._route_space['path'] = paths
        self._route_space['0'] = channel_0
        self._route_space['1'] = channel_1
        self._route_space['2'] = channel_2
        self._route_space['3'] = channel_3
        self._route_space['4'] = channel_4
        self._route_space['5'] = channel_5
        self._route_space['6'] = channel_6
        self._route_space['7'] = channel_7
        self._route_space['8'] = channel_8
        self._route_space['9'] = channel_9

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

            self._switching_matrix[node_label] = node_dict['switching_matrix']
            print("switching matrix ", self.switching_matrix)


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

    @property
    def route_space(self):
        return self._route_space

    @route_space.setter
    def route_space(self, route_space):
        self._route_space = route_space

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

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
            node.switching_matrix = {}
            for connected_node in node.connected_nodes:
                node.switching_matrix[connected_node] = {}
                for connected_node_i in node.connected_nodes:
                    if connected_node_i == connected_node:
                        node.switching_matrix[connected_node][connected_node_i] = np.zeros(10, np.int8)
                    else:
                        node.switching_matrix[connected_node][connected_node_i] = np.ones(10, np.int8)

                line_label = node_label + connected_node
                line = lines_dict[line_label]
                line.successive[connected_node] = nodes_dict[connected_node]
                node.successive[line_label] = lines_dict[line_label]

    def propagate(self, lightpath):
        start_node = self.nodes[lightpath.path[0]]
        propagated_signal_information = start_node.propagate(lightpath)
        return propagated_signal_information

    def find_best_snr(self, node_input, node_output):
        if node_input != node_output:
            my_df = self.weighted_path
            my_df.sort_values(by=['snr'], inplace=True, ascending=False)
            my_df_filtered = my_df[(my_df['path'].str[0] == node_input) & (my_df['path'].str[-1] == node_output)]
            for i in my_df_filtered.values:
                path = i[0]  # path
                channel = self.channel_free(path)
                if channel is not None:
                    return i, i[0], channel
        return None, None, None

    def channel_free(self, path):
        occupied = False
        node1 = path[3]
        first_line = self.lines[path[0] + node1]

        for index in range(10):
            node1 = path[3]
            if first_line.state[index] == 1:  # Free
                for node_i in range(6, len(path), 3):
                    line = self.lines[node1 + path[node_i]]
                    node1 = path[node_i]
                    if line.state[index] == 0:  # occupied
                        occupied = True
                        break
                if not occupied:
                    break
                occupied = False
        else:
            return None

        if not occupied:
            return index
        else:
            return None

    def find_best_latency(self, node_input, node_output):
        if node_input != node_output:
            my_df = self.weighted_path
            my_df.sort_values(by=['latency'], inplace=True, ascending=True)
            my_df_filtered = my_df[(my_df['path'].str[0] == node_input) & (my_df['path'].str[-1] == node_output)]
            for i in my_df_filtered.values:
                path = i[0]
                channel = self.channel_free(path)
                if channel is not None:
                    return i, i[0], channel
        return None, None, None

    def stream(self, connections, label='latency'):
        for connection in connections:
            if label == 'snr':
                best_path_array, best_path, channel = self.find_best_snr(connection.input, connection.output)
            else:
                best_path_array, best_path, channel = self.find_best_latency(connection.input, connection.output)

            if best_path is not None:
                path_label = ''
                for index in range(0, len(best_path), 3):
                    path_label += best_path[index]
                '''print("*****")
                print("BEST PATH: ", best_path)
                print("CHANNEL OCCUPIED: ", channel)
                print("*****")'''
                lightpath = Lightpath(connection.signal_power, path_label, channel)
                self.propagate(lightpath)
                # DEBUG: print("Noise :  ", lightpath.noise_power, path_label)
                connection.snr = self.snr_dB(lightpath.signal_power, lightpath.noise_power)
                connection.latency = lightpath.latency
            else:
                connection.snr = 0
                connection.latency = -1  # None

            if best_path is not None:
                if not (self.route_space.path.astype('str') == best_path).any():
                    row_route_space = [
                        {'path': best_path, '0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
                         '7': 1, '8': 1, '9': 1}]
                    new_df_route_space = pd.DataFrame.from_dict(row_route_space)
                    if (self.route_space.index.empty is True):
                        self.route_space = new_df_route_space.copy()
                    else:
                        self.route_space = self.route_space.append(new_df_route_space, ignore_index=True, sort=None)
                    current_index = self.route_space.index.max()

                else:
                    current_index = self.route_space[self.route_space['path'] == best_path].index.values[0]
                self.update_routing_space(best_path, channel, current_index)

    def snr_dB(self, signal_power, noise_power):
        return 10 * np.log10(signal_power / noise_power)

    def update_routing_space(self, best_path, channel, current_index):
        node1 = 3
        first_line = self.lines[best_path[0] + best_path[node1]]
        #print('path  ', best_path)
        result = first_line.state
        for node_i in range(6, len(best_path), 3):
            line = self.lines[best_path[node1] + best_path[node_i]]
            result = np.multiply(result, line.state)
            result = np.multiply(self.nodes[best_path[node1]].switching_matrix[best_path[node1-3]][best_path[node_i]], result)
            node1 = node_i
            #print(result)

        for i in range(10):
            self.route_space.at[current_index, str(i)] = result[i]
        #print(self.route_space)

