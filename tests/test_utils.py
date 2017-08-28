import unittest
from utils import matparser, data_compiler, model_tools


class TestDataCompiler(unittest.TestCase):
    pass


class TestMatlabParser(unittest.TestCase):
    pass


class TestModelTools(unittest.TestCase):
    def setUp(self):
        self.legit_csv = 'tests/test_data/legit.csv'

    def test_convergence(self):
        """
        Confirm that legitimate models successfully converge
        """
        legit_models = model_tools.gen_models(self.legit_csv, samples=3000)
        self.assertTrue(model_tools.check_convergence(legit_models))

    #def test_convergence_failure(self):
    #    """
    #    Confirm that bogus models fail to converge
    #    """
    #    return


if __name__ == '__main__':
    unittest.main()
