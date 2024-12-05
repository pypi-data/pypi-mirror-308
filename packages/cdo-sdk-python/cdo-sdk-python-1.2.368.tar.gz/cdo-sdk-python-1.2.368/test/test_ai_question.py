# coding: utf-8

"""
    CDO API

    Use the documentation to explore the endpoints CDO has to offer

    The version of the OpenAPI document: 1.0.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from cdo_sdk_python.models.ai_question import AiQuestion

class TestAiQuestion(unittest.TestCase):
    """AiQuestion unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AiQuestion:
        """Test AiQuestion
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AiQuestion`
        """
        model = AiQuestion()
        if include_optional:
            return AiQuestion(
                content = 'What's the difference between an Admin and a Super Admin?'
            )
        else:
            return AiQuestion(
        )
        """

    def testAiQuestion(self):
        """Test AiQuestion"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
