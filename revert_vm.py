#! /usr/bin/python

from pyVim.connect import SmartConnect, Disconnect
from pyVim.task import WaitForTasks
from pyVmomi import vim
import ssl

s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE
vm_names = ["vm-a", "vm-b", "vm-c", "vm-d"]
snapshot_name = "init_snapshot"

connection = SmartConnect(host="10.0.0.100", user="user1@vsphere.local",
                          pwd="passw0rd", sslContext=s)

vms=[]

for name in vm_names:
    entity_stack = connection.content.rootFolder.childEntity
    while entity_stack:
        entity = entity_stack.pop()
        if entity.name == name:
            vms.append(entity)
            del entity_stack[0:len(entity_stack)]
        elif hasattr(entity, 'childEntity'):
            entity_stack.extend(entity.childEntity)
        elif isinstance(entity, vim.Datacenter):
            entity_stack.append(entity.vmFolder)

def get_snapshots_by_name_recursively(snapshots, snapname):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.name == snapname:
            snap_obj.append(snapshot)
        else:
            snap_obj = snap_obj + get_snapshots_by_name_recursively\
                       (snapshot.childSnapshotList, snapname)
    return snap_obj

for vm in vms:
    if vm.name in vm_names:
        snap_obj = get_snapshots_by_name_recursively\
                   (vm.snapshot.rootSnapshotList, snapshot_name)
        print("Reverting snapshot:", snap_obj[0].name, "for vm:", vm.name)
        task = [snap_obj[0].snapshot.RevertToSnapshot_Task()]
        WaitForTasks(task, connection)

Disconnect(connection)
