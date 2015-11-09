from mininet.topo import Topo

class clos(Topo):

    def __init__(self, leaf, spine):
        Topo.__init__(self)

        spineDevs = self.create_devices(self.addSwitch, "ss", spine)
        leafDevs = self.create_devices(self.addSwitch, "ls", leaf)
        hostDevs = self.create_devices(self.addHost, "h", leaf)

        self.hookup(spineDevs, leafDevs, hostDevs)

    def create_devices(self, addFunc, prefix, nofDevices):
        devices = list()

        for devID in range(0, nofDevices):
            devices.append( addFunc( prefix + str(devID + 1) ) )

        return devices

    def hookup(self, spineDevices, leafDevices, hostDevices):
        leafIndex = 0
        for ldev in leafDevices:
            hdev = hostDevices[leafIndex]
            self.addLink(ldev, hdev)
            hdev.setIP("10.0.0." + str(leafIndex + 1), 24)
            leafIndex += 1
            for sdev in spineDevices:
                self.addLink(ldev, sdev)


topos = { 'clos': clos }
