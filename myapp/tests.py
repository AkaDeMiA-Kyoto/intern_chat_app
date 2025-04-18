from django.test import TestCase


# Create your tests here.
class ExampleTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super.setUpClass()

    @classmethod
    def tearDownClass(cls):
        # 具体的な処理
        super.tearDownClass()

    def setUp(self):
        # 具体的な処理
        pass

    def tearDown(self):
        # 具体的な処理
        pass

    def test_hoge(self):
        # 具体的な処理
        pass

    def test_huga(self):
        # 具体的な処理
        pass
