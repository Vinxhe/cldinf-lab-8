from mininet.topo import Topo
from mininet.node import OVSSwitch

class OVSBridgeSTP( OVSSwitch ):
    prio = 1000
    def start( self, *args, **kwargs ):
        OVSSwitch.start( self, *args, **kwargs )
        OVSBridgeSTP.prio += 1
        self.cmd( 'ovs-vsctl set-fail-mode', self, 'standalone' )
        self.cmd( 'ovs-vsctl set Bridge', self,
                  'stp_enable=true',
                  'other_config:stp-priority=%d' % OVSBridgeSTP.prio )

switches = { 'ovs-stp': OVSBridgeSTP }

class clos(Topo):

    def __init__(self, leaf, spine):
        Topo.__init__(self)

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
                devices.append( addFunc( prefix + str(devID + 1), cls=OVSBridgeSTP ) )
        return devices

    def hookup(self, spineDevices, leafDevices, hostDevices):
        leafIndex = 0
        for ldev in leafDevices:
            hdev = hostDevices[leafIndex]
            self.addLink(ldev, hdev)
            leafIndex += 1
            for sdev in spineDevices:
                self.addLink(ldev, sdev)

topos = { 'clos': clos }
