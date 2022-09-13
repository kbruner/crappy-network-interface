#!/usr/bin/env python3

import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from freebsd_cni import *

import unittest
from unittest import mock

class TestCNIRequest(unittest.TestCase):
    """
    CNIRequest is all about environment variables
    """

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add(self):
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            self.assertTrue(request.command == "ADD")
            return_error.assert_not_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del(self):
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            self.assertTrue(request.command == "DEL")
            return_error.assert_not_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    def test_del_missing_env_var(self):
        # required var CNI_IFNAME is missing
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            return_error.assert_called()



class TestCNIConfig(unittest.TestCase):
    """
    CNIConfig reads/parses input JSON
    """

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add_no_input(self):
        with mock.patch("freebsd_cni.return_error") as return_error:
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
    def test_del_wrong_input(self):
        f = open("add_input.json", "r")
        input = f.read()
        f.close()
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            cni = CNIConfig(input, request)
            return_error.assert_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add_correct_input(self):
        f = open("add_input.json", "r")
        input = f.read()
        f.close()
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            cni = CNIConfig(input, request)
            return_error.assert_not_called()
            self.assertEqual(cni.subnet, "172.16.0.0/24")
            self.assertIsInstance(cni.config, dict)

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del_correct_input(self):
        f = open("del_input.json", "r")
        input = f.read()
        f.close()
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            cni = CNIConfig(input, request)
            return_error.assert_not_called()
            self.assertIsInstance(cni.prev_result, dict)


class TestFreeBSDNetIf(unittest.TestCase):
    def test_gen_mac_addr(self):
        mac_addr = FreeBSDNetIf.gen_mac_addr()
        self.assertRegex(mac_addr,
                r'^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')



if __name__ == "__main__":
    unittest.main()
