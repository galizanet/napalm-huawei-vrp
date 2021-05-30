# Copyright 2016 Dravetech AB. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""Tests."""

import unittest

from unittest import SkipTest

from napalm.base.test import models
from napalm.base.test.base import (
    TestConfigNetworkDriver,
    TestGettersNetworkDriver
)

from napalm.base.test.double import BaseTestDouble

from napalm_huawei_vrp import VRPDriver

import json


class TestConfigHuaweiVRPDriver(unittest.TestCase, TestConfigNetworkDriver):
    """Group of tests that test Configuration related methods."""

    @classmethod
    def setUpClass(cls):
        """Run before starting the tests."""
        hostname = '127.0.0.1'
        username = 'vagrant'
        password = 'vagrant'
        cls.vendor = 'huawei_vrp'

        optional_args = {}
        cls.device = huawei.VRPDriver(
            hostname, username, password, timeout=60, optional_args=optional_args)
        cls.device.open()

        cls.device.load_replace_candidate(
            filename='%s/initial.conf' % cls.vendor)
        cls.device.commit_config()

    def test_huawei_vrp_only_confirm(self):
        """Test _disable_confirm() and _enable_confirm().
        _disable_confirm() changes router config
                                    so it doesn't prompt for confirmation
        _enable_confirm() reenables this
        """
        # Set initial device configuration
        self.device.load_merge_candidate(
            filename='%s/initial.conf' % self.vendor)
        self.device.commit_config()

    def test_huawei_vrp_only_check_file_exists(self):
        """Test _check_file_exists() method."""
        self.device.load_merge_candidate(
            filename='%s/initial.conf' % self.vendor)
        valid_file = self.device._check_file_exists('salt_merge_config.txt')
        self.assertTrue(valid_file)
        invalid_file = self.device._check_file_exists('bogus_999.txt')
        self.assertFalse(invalid_file)


class TestGetterDriver(unittest.TestCase, TestGettersNetworkDriver):
    """Group of tests that test getters."""

    @classmethod
    def setUpClass(cls):
        """Run before starting the tests."""
        cls.mock = True

        hostname = '127.0.0.1'
        username = 'vagrant'
        password = 'vagrant'
        cls.vendor = 'skeleton'

        optional_args = {'port': 12443, }
        cls.device = vrp.VRPDriver(hostname, username, password, timeout=60,
                                   optional_args=optional_args)

        if cls.mock:
            cls.device.device = FakeDevice()
        else:
            cls.device.open()


class FakeHuaweiVRPDevice:
    """Class to fake a Huawei VRP device."""

    @staticmethod
    def read_json_file(filename):
        """Return the content of a file with content formatted as json."""
        with open(filename) as data_file:
            return json.load(data_file)

    @staticmethod
    def read_txt_file(filename):
        """Return the content of a file."""
        with open(filename) as data_file:
            return data_file.read()

    def send_command_expect(self, command, **kwargs):
        """Fake execute a command in the device by just returning the
        content of a file."""
        # cmd = re.sub(r'[\[\]\*\^\+\s\|/]', '_', command)
        cmd = '{}'.format(BaseTestDouble.sanitize_text(command))
        file_path = 'huawei_vrp/mock_data/{}.txt'.format(cmd)
        print("file_path :: " + file_path)
        output = self.read_txt_file(file_path)
        return str(output)

    def send_command(self, command, **kwargs):
        """Fake execute a command in the device by just
        returning the content of a file."""
        return self.send_command_expect(command)

    def set_base_prompt(self, pri_prompt_terminator='#',
                        alt_prompt_terminator='>', delay_factor=1):
        return "#"
