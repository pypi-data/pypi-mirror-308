# tests/test_primeiroPypi.py

import unittest
from primeiroPypi import imprime_Hello_world, faz_de_novo

class TestPrimeiroPypi(unittest.TestCase):

    def test_imprime_Hello_world(self):
        self.assertAlmostEqual(imprime_Hello_world, 50.0)

    def test_faz_de_novo(self):
        self.assertAlmostEqual(faz_de_novo, 1338.23, places=2)

if __name__ == '__main__':
    unittest.main()

