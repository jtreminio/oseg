import unittest
from random import randrange

from oseg import parser
from test_utils import TestUtils
from fixtures.mock_extension import MockExtension


class TestTemplateParser(unittest.TestCase):
    oa_parser: parser.OaParser

    @classmethod
    def setUpClass(cls) -> None:
        cls.oa_parser = TestUtils.oa_parser("template_parser")
        cls.extension = MockExtension()
        cls.template_parser = cls.extension.template_parser
