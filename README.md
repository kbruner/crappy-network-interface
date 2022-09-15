# Crappy Network Interface

WIP


A very non-compliant implementation of the [Container Network
Interface](https://www.cni.dev/)
[spec](https://www.cni.dev/plugins/current/ipam/static/) for use with the very
experimental FreeBSD containerd, particularly with use with Linux containers
running in emulation mode of FreeBSD. Implemented in python.

NOTE: Upstream hooks in `runj` and `containerd` for FreeBSD support are still
WIP, so this plugin is just a PoC/personal project.

For some background, see [this
post](https://productionwithscissors.run/2022/09/04/containerd-linux-on-freebsd/)

The Container Network Interface specifications seems to be built on the
premise that plugins will be standalone binaries.
This implementations tries to be as self-contained as possible for minimal
installation requirements and steps. Deliberately uses no non-standard Python
modules and inline custom Classes so the only external dependency to
installation is Python3.9+ itself.


## TODO
* Implement `portmap` support
* Implement unique IP/device number selection
* Add Linux support?

## INSTALLATION
* Requirement: Python version >= 3.9. On FreeBSD, you may need to create the
  symbolic link from `python3.x` to `python3`
* BACK UP EXISTING FILES FIRST!

```
mkdir -p /opt/cni/bin /etc/cni/net.d
cp bridge /opt/cni/bin/bridge
cp 10-bridge.conflist /etc/cni/net.d/10-bridge.conflist
```

See `bridge` for inline comments.

# Create bridge device

## FreeBSD

Change parameters if using a different subnet or network device

1. `ifconfig bridge0 create`
2. `ifconfig bridge0 add em0`
3. `ifconfig bridge0 inet 172.16.0.0/24`
4. `ifconfig bridge0 alias 172.16.0.1/32`
5. `ifconfig bridge0 up`
 

## Linux

1. `ip link add name br0 type bridge`
2. `ip link set dev br0 up`
3. `ip addr add dev br0 172.16.0.1/24`
 
