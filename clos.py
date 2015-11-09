from mininet.topo import Topo

class clos(Topo):

    def __init__(self, leaf, spine):
        Topo.__init__(self)

        spineDevs = self.create_spine(spine)
        leafDevs = self.create_leaf(leaf)

        self.hookup(spineDevs, leafDevs)

    def create_spine(self, nofDevices):
        return []

    def create_leaf(self, nofDevices):
        return []

    def hookup(self, spineDevices, leafDevices):
        pass

topos = { 'clos': clos }
