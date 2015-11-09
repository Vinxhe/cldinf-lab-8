from mininet.topo import Topo

class clos(Topo):

    def __init__(self, leaf, spine):
        print(leaf)
        print(spine)

topos = { 'clos': clos }
