from Lab07.core.Info.Lightpath import Lightpath

class Node(object):
    def __init__(self, node_dict):
        self._label = node_dict['label']
        self._position = node_dict['position']
        self._connected_nodes = node_dict['connected_nodes']
        self._successive = {}
        self._switching_matrix = None

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

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

    def propagate(self, lighpath, previous_node):
        path = lighpath.path
        if len(path) > 1:
            line_label = path[:2]
            #ABD B
            if type(lighpath) is Lightpath:
                if previous_node is not None:
                 channels = self.switching_matrix[previous_node][line_label[1]]
                 channels[lighpath.channel] = 0
                 if lighpath.channel != 9:
                    channels[lighpath.channel+1] = 0
                 if lighpath.channel != 0:
                    channels[lighpath.channel-1] = 0

            line = self.successive[line_label]
            lighpath.next()
            lighpath = line.propagate(lighpath)
        return lighpath


