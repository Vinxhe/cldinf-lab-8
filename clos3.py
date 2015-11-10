from mininet.topo import Topo

class clos3(Topo):

    def __init__(self, leaf, spine):

        # Initialize topology
        Topo.__init__( self )

        spineDevs = self.create_devices(self.addSwitch, "ss", spine, False)
        leafDevs = self.create_devices(self.addSwitch, "ls", leaf, False )
        hostDevs = self.create_devices(self.addHost, "h", leaf, True )

        self.hookup(spineDevs, leafDevs, hostDevs)

    def create_devices(self, addFunc, prefix, nofDevices, withIP ):
        devices = list()

        for devID in range(0, nofDevices):
            if (withIP == True):
                devices.append( addFunc( prefix + str(devID + 1), ip='10.0.0.' + str(devID + 1) ) )
            else:
                devices.append( addFunc( prefix + str(devID + 1) ) )

        return devices

    def hookup(self, spineDevices, leafDevices, hostDevices):
        leafIndex = 0
        for ldev in leafDevices:
            hdev = hostDevices[leafIndex]
            self.addLink(ldev, hdev)
            #hdev.setIP("10.0.0." + str(leafIndex + 1), 24)
            leafIndex += 1
            for sdev in spineDevices:
                self.addLink(ldev, sdev)

topos = { 'clos3': clos3 }
