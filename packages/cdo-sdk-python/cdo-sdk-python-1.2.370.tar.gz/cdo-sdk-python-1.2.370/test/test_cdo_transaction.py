# coding: utf-8

"""
    Cisco Defense Orchestrator API

    Use the interactive documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 0.0.1
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.models.cdo_transaction import CdoTransaction

class TestCdoTransaction(unittest.TestCase):
    """CdoTransaction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CdoTransaction:
        """Test CdoTransaction
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CdoTransaction`
        """
        model = CdoTransaction()
        if include_optional:
            return CdoTransaction(
                transaction_uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb',
                tenant_uid = '5131daad-e813-4b8f-8f42-be1e241e2cdb',
                entity_uid = 'f5f660d4-4b81-4374-877d-fbc4bee894e2',
                entity_url = 'https://edge.us.cdo.cisco.com/platform/public-api/v1/inventory/devices/f5f660d4-4b81-4374-877d-fbc4bee894e2',
                transaction_polling_url = 'https://edge.us.cdo.cisco.com/platform/public-api/v1/transactions/7131daad-e813-4b8f-8f42-be1e241e8cdb',
                submission_time = '2023-12-13T05:15:44Z',
                last_updated_time = '2023-12-13T08:15:44Z',
                transaction_type = 'ONBOARD_ASA',
                cdo_transaction_status = 'IN_PROGRESS',
                error_message = '',
                error_details = {
                    'key' : ''
                    }
            )
        else:
            return CdoTransaction(
        )
        """

    def testCdoTransaction(self):
        """Test CdoTransaction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
