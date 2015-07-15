import unittest
from tmc import points


@points('1.1')
class TestFailing(unittest.TestCase):

    @points('1.2', '2.2')
    def test_new(self):
        self.assertEqual("a", "b");

if __name__ == '__main__':
    unittest.main()
