# base
from base.tests import BaseTestCase

# models
from parameters.models import Parameter

# enums
from parameters.enums import ParameterDefinitionList


class ParameterTestCase(BaseTestCase):
    def test_create_all_parammeters(self):
        Parameter.create_all_parameters()
        self.assertEqual(
            Parameter.objects.count(),
            len(ParameterDefinitionList.definitions)
        )
