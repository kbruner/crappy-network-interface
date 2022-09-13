#!/usr/bin/env python3

import importlib.util
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import freebsd_cni
from freebsd_cni import CNIRequest

import unittest
from unittest import mock



class TestCNIRequest(unittest.TestCase):

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "ADD"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_add(self):
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            self.assertTrue(request.command == "ADD")
            freebsd_cni.return_error.assert_not_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    @mock.patch.dict(os.environ, {"CNI_IFNAME": "eth0"})
    def test_del(self):
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            self.assertTrue(request.command == "DEL")
            freebsd_cni.return_error.assert_not_called()

    @mock.patch.dict(os.environ, {"CNI_COMMAND": "DEL"})
    @mock.patch.dict(os.environ, {"CNI_CONTAINERID": "blah"})
    @mock.patch.dict(os.environ, {"CNI_NETNS": "superblah"})
    def test_del_missing_env_var(self):
        with mock.patch("freebsd_cni.return_error") as return_error:
            request = CNIRequest()
            freebsd_cni.return_error.assert_called()



if __name__ == "__main__":
    unittest.main()
