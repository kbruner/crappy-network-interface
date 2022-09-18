#!/usr/bin/env python3

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from cni import *

import unittest
from unittest import mock

@mock.patch("cni.return_error")
class TestCNIRequest(unittest.TestCase):
    """
    CNIRequest is all about environment variables
    """

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add(self, return_error):
        request = CNIRequest()
        self.assertTrue(request.command == "ADD")
        return_error.assert_not_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del(self, return_error):
        request = CNIRequest()
        self.assertTrue(request.command == "DEL")
        return_error.assert_not_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    def test_del_missing_env_var(self, return_error):
        # required var CNI_IFNAME is missing
        request = CNIRequest()
        return_error.assert_called()



@mock.patch("cni.return_error")
class TestCNIConfig(unittest.TestCase):
    """
    CNIConfig reads/parses input JSON
    """

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add_no_input(self, return_error):
        input = ''
        request = CNIRequest()
        try:
            cni = CNIConfig(input, request)
        except AttributeError:
            return
        return_error.assert_called()


    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del_wrong_input_freebsd(self, return_error):
        f = open("add_input_freebsd.json", "r")
        input = f.read()
        f.close()
        request = CNIRequest()
        cni = CNIConfig(input, request)
        return_error.assert_called()


    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del_wrong_input_linux(self, return_error):
        f = open("add_input_linux.json", "r")
        input = f.read()
        f.close()
        request = CNIRequest()
        cni = CNIConfig(input, request)
        return_error.assert_called()


    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add_correct_input_freebsd(self, return_error):
        f = open("add_input_freebsd.json", "r")
        input = f.read()
        f.close()
        request = CNIRequest()
        cni = CNIConfig(input, request)
        return_error.assert_not_called()
        self.assertEqual(cni.subnet, "172.16.0.0/24")
        self.assertIsInstance(cni.config, dict)
        self.assertFalse(request.noop)


    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add_correct_input_linux(self, return_error):
        f = open("add_input_linux.json", "r")
        input = f.read()
        f.close()
        request = CNIRequest()
        cni = CNIConfig(input, request)
        return_error.assert_not_called()
        self.assertEqual(cni.subnet, "172.16.0.0/24")
        self.assertIsInstance(cni.config, dict)
        self.assertFalse(request.noop)


    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del_correct_input(self, return_error):
        f = open("del_input.json", "r")
        input = f.read()
        f.close()
        request = CNIRequest()
        cni = CNIConfig(input, request)
        return_error.assert_not_called()
        self.assertIsInstance(cni.prev_result, dict)



class TestNetIf(ABC, unittest.TestCase):
    def test_gen_mac_addr(self):
        mac = NetIf.gen_mac_addr()
        self.assertRegex(mac,
                r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')


    def test_fix_netmask(self):
        cidr = NetIf.fix_netmask("255.255.254.0")
        self.assertEqual(cidr, 23)



@mock.patch("cni.return_error")
class TestFreeBSDNetIf(unittest.TestCase):
        @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        @mock.patch("cni.subprocess.run")
        def test_allocate(self, run, return_error):
            request = CNIRequest()
            f = open("add_input_freebsd.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = FreeBSDNetIf(cni, request)
            netif.allocate()
            self.assertRegex(netif.virtual_if.device, r'^[a-z]+\d+')


        @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        @mock.patch("cni.subprocess.run")
        def test_new_ip(self, run, return_error):
            request = CNIRequest()
            f = open("add_input_freebsd.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = FreeBSDNetIf(cni, request)
            netif.new_ip()
            self.assertRegex(netif.container_if.ip,
                    r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2}')


        @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        @mock.patch("cni.subprocess.run")
        def test_create(self, run, return_error):
            request = CNIRequest()
            f = open("add_input_freebsd.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = FreeBSDNetIf(cni, request)

            with mock.patch("cni.os.system") as mock_system:
                netif.create()
                mock_system.assert_called()
                return_error.assert_not_called()
                self.assertRegex(netif.container_if.ip,
                    r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2}')


        @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        @mock.patch.dict(os.environ, {"NOOP": "True"})
        def test_del_noop(self, return_error):
            request = CNIRequest()
            f = open("del_input.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = FreeBSDNetIf(cni, request)

            with mock.patch("cni.os.system") as mock_system:
                netif.delete()
                mock_system.execute.assert_not_called()
                return_error.assert_not_called()



@mock.patch("cni.return_error")
class TestLinuxNetIf(unittest.TestCase):
        @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        def test_allocate(self, return_error):
            request = CNIRequest()
            f = open("add_input_linux.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = LinuxNetIf(cni, request)
            netif.allocate()
            self.assertRegex(netif.virtual_if.device, r'^[a-z]+\w+')


        @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        def test_new_ip(self, return_error):
            request = CNIRequest()
            f = open("add_input_linux.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = LinuxNetIf(cni, request)
            netif.new_ip()
            self.assertRegex(netif.container_if.ip,
                    r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2}')


        @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        @mock.patch("cni.subprocess.run")
        def test_create(self, run, return_error):
            request = CNIRequest()
            f = open("add_input_linux.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = LinuxNetIf(cni, request)

            with mock.patch("cni.os.system") as mock_system:
                netif.create()
                run.assert_called()
                mock_system.assert_called()
                return_error.assert_not_called()
                self.assertRegex(netif.container_if.ip,
                    r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}/\d{1,2}')


        @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
        @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
        @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
        @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
        @mock.patch.dict(os.environ, {"NOOP": "True"})
        @mock.patch("cni.subprocess.run")
        def test_del_noop(self, return_error, run):
            request = CNIRequest()
            f = open("del_input.json", "r")
            input = f.read()
            f.close()
            cni = CNIConfig(input, request)
            netif = LinuxNetIf(cni, request)

            with mock.patch("cni.os.system") as mock_system:
                netif.delete()
                mock_system.execute.assert_not_called()
                run.assert_not_called()
                return_error.assert_not_called()



class TestAddResult(unittest.TestCase):
    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    @mock.patch.dict(os.environ, {"NOOP": "true"})
    def test_create_freebsd(self):
        request = CNIRequest()
        f = open("add_input_freebsd.json", "r")
        input = f.read()
        f.close()
        cni = CNIConfig(input, request)
        netif = FreeBSDNetIf(cni, request)

        result = AddResult(cni, request, netif)
        result.set_if_result(netif.container_if)

        output = result.json_output()
        try:
            json.loads(output)
        except ValueError:
            self.fail("AddResult output is not valid JSON")


    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    @mock.patch.dict(os.environ, {"NOOP": "true"})
    def test_create_linux(self):
        request = CNIRequest()
        f = open("add_input_linux.json", "r")
        input = f.read()
        f.close()
        cni = CNIConfig(input, request)
        netif = LinuxNetIf(cni, request)

        result = AddResult(cni, request, netif)
        result.set_if_result(netif.container_if)

        output = result.json_output()
        try:
            json.loads(output)
        except ValueError:
            self.fail("AddResult output is not valid JSON")



if __name__ == "__main__":
    unittest.main()
