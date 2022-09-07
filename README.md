# Crappy Network Interface

WIP


A very non-compliant implementation of the [Container Network
Interface](https://www.cni.dev/)
[spec](https://www.cni.dev/plugins/current/ipam/static/) for use with the very
experimental FreeBSD containerd, particularly with use with Linux containers
running in emulation mode of FreeBSD. Implemented in python.

For some background, see [this
post](https://productionwithscissors.run/2022/09/04/containerd-linux-on-freebsd/)

TODO:
- Implement parsing/using config from `/etc/cni/net.d/*`
- Implement `DEL`
- Implement `portmap` support
- Test the thing

See `bridge` for inline comments.
