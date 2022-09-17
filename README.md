# Crappy Network Interface

A very non-compliant implementation of the [Container Network
Interface](https://www.cni.dev/) plugin 
[spec](https://www.cni.dev/plugins/current/ipam/static/)

(Basically) works on Linux with `runc` and `containerd`.

## Background

The Container Network Interface specifications seems to be built on the
premise that plugins will be standalone binaries.
This implementations tries to be as self-contained as possible for minimal
installation requirements and steps. Deliberately uses no non-standard Python
modules and inline custom Classes so the only external dependency to
installation is Python3.9+ itself.

Originally this was for use with the very experimental FreeBSD containerd,
particularly with use with Linux containers running in emulation mode on
FreeBSD. However, upstream hooks in `runj` and `containerd` for FreeBSD
support are still WIP, so this plugin is just a PoC/personal project. For some background, see [this
post](https://productionwithscissors.run/2022/09/04/containerd-linux-on-freebsd/)

## TODO

* Implement unique IP selection (oops)
* Implement `portmap` support?
* (update tests)
* (link)

## Warning!

**Note**: This is totally insecure and broken. Do not do any of this! **USE AT
YOUR OWN RISK**

Change parameters if using a different subnet or network device

## Installation

* Requirement: Python version >= 3.9 as `python3`
* BACK UP EXISTING FILES FIRST!

On Linux:
```
mkdir -p /opt/cni/bin /etc/cni/net.d
cp cni /opt/cni/bin/cni
cp 10-cni-linux.conflist /etc/cni/net.d/10-cni.conflist
```

## System setup

### Create the bridge device

1. `ip link add name br0 type bridge`
2. `ip link set dev br0 up`
3. `ip addr add dev br0 172.16.0.1/24`

### Share hosts's `systemd-resolved` DNS resolver with bridged containers

1. Add `DNSStubListenerExtra=172.16.0.1` to /etc/systemd/resolved.conf
2. `systemctl restart resolved`

`runc` ignores the CNI dns param, so to use the bridged resolved, pass
`--dns 172.16.0.1` to `nerdctl run` (or `docker run`, you do you)

### Add NAT to read the Internet from bridged network

TBD
