
class Node(object):
    def __init__(self, node_dict):
        self._label = node_dict['label']
        self._position = node_dict['position']
        self._connected_nodes = node_dict['connected_nodes']
        self._successive = {}

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

    def propagate(self, lighpath):
        path = lighpath.path
        if len(path) > 1:
            line_label = path[:2]
            line = self.successive[line_label]
            lighpath.next()
            lighpath = line.propagate(lighpath)
        return lighpath


