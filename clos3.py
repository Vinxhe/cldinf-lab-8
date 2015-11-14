#!/usr/bin/python

import os, sys
from mininet.net import Mininet
from mininet.node import OVSSwitch, OVSController, Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.util import quietRun
from mininet.moduledeps import pathCheck

class clos3(Topo):

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
                devices.append( addFunc( prefix + str(devID + 1) ) )
        return devices

    def hookup(self, spineDevices, leafDevices, hostDevices):
        leafIndex = 0
        for ldev in leafDevices:
            hdev = hostDevices[leafIndex]
            self.addLink(ldev, hdev)
            leafIndex += 1
            for sdev in spineDevices:
                self.addLink(ldev, sdev)

topos = { 'clos3': clos3 }

class MyController( Controller ):

    def __init__( self, name, inNamespace=False, command='controller',
                 cargs='-v ptcp:%d', cdir=None, ip="127.0.0.1",
                 port=6633, **params ):
        """command: controller command name
           cargs: controller command arguments
           cdir: director to cd to before running controller
           ip: IP address for controller
           port: port for controller to listen at
           params: other params passed to Node.__init__()"""
        Controller.__init__( self, name, ip=ip, port=port, **params)

    def start( self ):
        """Start <controller> <args> on controller.
            Log to /tmp/cN.log"""
        pathCheck( self.command )
        cout = '/tmp/' + self.name + '.log'
        if self.cdir is not None:
            self.cmd( 'cd ' + self.cdir )
        self.cmd( self.command, self.cargs % self.port, '>&', cout, '&' )

    def stop( self ):
        "Stop controller."
        self.cmd( 'kill %' + self.command )
        self.terminate()

def layer3net(leaf, spine):
    if os.geteuid() != 0:
        exit("you need to be root to run this script")
    topo = clos3(leaf, spine)
    info( '*** Creating network\n' )
    net = Mininet(topo=topo, controller=OVSController, switch=OVSSwitch)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    layer3net(int(sys.argv[1]),int(sys.argv[2]))
