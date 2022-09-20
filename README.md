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


## Limitations / TODO

* IPv4 only, no IPv6 support
* Implement unique IP selection
* No `portmap` support
* Support more than one interface (incorrectly assumes there will be only one)

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

*THIS IS TOTALLY INSECURE, DO NOT DO THIS*

Change IP addresses and device names as needed

1. `sysctl -w net.ipv4.ip_forward=1`
2. `sysctl -w net.ipv4.conf.all.forwarding=1`
3. `iptables -P FORWARD ACCEPT`
4. `iptables -P INPUT ACCEPT`
5. `iptables -P OUTPUT ACCEPT`
6. `iptables -t nat -A POSTROUTING -s 172.16.0.0/24 ! -o br0 -j MASQUERADE`

If you only want to NAT for one container, you can replace `172.16.0.0/24`
with the host's `/32` IP address.

If this doesn't work, you can try running `iptables -t nat --flush` first and
then reapply the `iptables` rules above, but I don't recommend it.


## References
* https://www.cni.dev/docs/spec/
* https://karampok.me/posts/container-networking-with-cni/
* https://github.com/s-matyukevich/bash-cni-plugin
* https://andreaskaris.github.io/blog/openshift/analyzing-cni/
