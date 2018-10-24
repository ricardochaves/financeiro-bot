from django.test import TestCase
from mainapp.models import ModelExample
# Create your tests here.


class ModelExampleTestCase(TestCase):
    def setUp(self):
        pass

    def test_createmodel(self):
        """Test: Should create model"""

        modelexemple = ModelExample.objects.create(title="oi", content="teste")
        self.assertEqual(modelexemple.title, "oi")
