# Copyright (c) Trainline Limited, 2017. All rights reserved. See LICENSE.txt in the project root for license information.

import responses
import random
import string
import os

from unittest import TestCase
from emcli.commands import PatchCommand
from nose_parameterized import parameterized, param
from mock import patch
from .helpers.api_test_case import APITestCase
from .helpers.utils import mock_server, MOCK_ENV_VARS
from .helpers.patch_scenarios import TEST_SCENARIOS

class PatchTest(APITestCase):

    @parameterized.expand( TEST_SCENARIOS )
    @responses.activate
    @patch.dict(os.environ, MOCK_ENV_VARS)
    def test_get_patch_requirements(self, *args, **kwargs):
        patch_cluster = kwargs.get('patch_cluster')
        expected_result = kwargs.get('expected')
        from_ami = kwargs.get('from_ami')

        servers_in_env = []
        self.mock_response(r'/asgs/[\w\.\-]+', {'AvailabilityZones':[1]})
        self.mock_response(r'/environments/[\w\.\-]+/servers/[\w\.\-]+', 
            {'ServicesCount':{'Expected':2}, 'Instances':[{'RunningServicesCount':2}]}
        )

        # Create a list of servers in env, based on test scenario
        for server_desc in args:
            servers_in_env += self.create_servers(**server_desc)

        self.setup_responses()
        self.respond_with_servers(servers_in_env)

        sut = PatchCommand({})
        result = sut.get_patch_requirements( **{
            'cluster':patch_cluster,
            'env':'staging',
            'from_ami':from_ami 
        })
        self.assertEqual(len(list(result)), expected_result)
    

    def respond_with_servers(self, servers):
        server_response = {
            'EnvironmentName': 'staging',
            'Value': servers
        }
        self.mock_response(r'/environments/[\w\.\-]+/servers', server_response)

    def setup_responses(self):
        self.mock_authentication()
        self.mock_response_with_file(r'/images', 'ami_response.json')

    def create_servers(self, cluster, n=1, ami='mock-ami-1.0.0', latest=False):
        servers = [ mock_server(cluster, ami, latest) for x in range(n) ]
        return servers

