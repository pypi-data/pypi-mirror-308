# coding: utf-8

"""
    CDO API

    Use the documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 1.1.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.models.access_rule_update_input import AccessRuleUpdateInput

class TestAccessRuleUpdateInput(unittest.TestCase):
    """AccessRuleUpdateInput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessRuleUpdateInput:
        """Test AccessRuleUpdateInput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessRuleUpdateInput`
        """
        model = AccessRuleUpdateInput()
        if include_optional:
            return AccessRuleUpdateInput(
                uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb',
                index = 1,
                rule_action = 'PERMIT',
                protocol = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                source_port = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                destination_port = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                source_network = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                destination_network = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                source_dynamic_object = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                destination_dynamic_object = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                log_settings = cdo_sdk_python.models.log_settings.LogSettings(
                    level = '3', 
                    interval = 1, ),
                rule_time_range = cdo_sdk_python.models.access_rule_details_content.AccessRuleDetailsContent(
                    name = 'any', 
                    uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb', 
                    type = 'NETWORK_OBJECT', 
                    elements = [
                        ''
                        ], ),
                remark = '',
                is_active_rule = False
            )
        else:
            return AccessRuleUpdateInput(
                uid = '7131daad-e813-4b8f-8f42-be1e241e8cdb',
        )
        """

    def testAccessRuleUpdateInput(self):
        """Test AccessRuleUpdateInput"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
