#! /usr/bin/python

from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTasks
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE
vm_names = ["vm-a", "vm-b", "vm-c", "vm-d"]
snapshot_name = "init_snapshot"

connection = SmartConnect(host="10.0.0.100", user="user1@vsphere.local",
                          pwd="passw0rd", sslContext=s)

vms = connection.content.rootFolder.childEntity[0].vmFolder.childEntity[0]\
      .childEntity[0].childEntity

for vm in vms:
    if vm.name in vm_names:
        print vm.name
        snapshots = vm.snapshot.rootSnapshotList
        for snapshot in snapshots:
            if snapshot_name == snapshot.name:
                snap_obj = snapshot.snapshot
                print "Reverting snapshot:", snapshot.name, "for vm:", vm.name
                task = [snap_obj.RevertToSnapshot_Task()]
                WaitForTasks(task, connection)

Disconnect(connection)
