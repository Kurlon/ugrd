__author__ = "Kurlon"
__version__ = "0.0.1"

def nbd_import(self) -> list[str]:
    """ Retruns bash lines to attach NBD volumes.
    
    One nbd-client command is returned per volume defined. Volumes
    tagged as swap will emit an additional line to enable swap on
    them.

    Define volumes as follows:
    [nbd.rootfs]
    host = "192.168.192.101"
    port = "9997"
    dev  = "0"
    swap = true

    Object names are purely descriptive to aid the user in
    keeping track of what they're configuring.

    The host is either an IP address or hostname. If using a
    hostname you will need to ensure your startup environment
    can resolve DNS to IPs, for example by using dhcpcd.

    The port will be unique per volume shared on a given server
    if using classic style NBD sharing.

    The dev specifies which /dev/nbdN to attach the volume to.

    The swap flag defaults to false, set it to true if you want
    swap enabled on the configured volume.
    """

    nbd = self["nbd"]

    attach_cmds = [] 

    for x, obj in nbd.items():
        attach_str = f"nbd-client {obj['host']} {obj['port']} /dev/nbd{obj['dev']} -persist -systemd-mark"
        if "swap" in obj:
            # Tell nbd-client it's a swap device
            attach_str += f" -swap"

            # Enable swap on this volume
            attach_str += f" && swapon /dev/nbd{obj['dev']}"

        attach_cmds.append(attach_str)

    return attach_cmds
