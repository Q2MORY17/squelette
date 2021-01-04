import unittest
from launcher import Launcher

class TestLauncher(unittest.TestCase):

    def setUp(self):
        self.lnchr = Launcher()

    def tearDown(self):
        pass

    def test_master(self):
        self.assertEqual(self.lnchr.pitch.status()[0], 1)
        self.assertEqual(self.lnchr.rotation.status()[0], 1)

    def test_slave1(self):
        self.assertEqual(self.lnchr.lift.status()[0], 1)
        self.assertEqual(self.lnchr._launch.status()[0], 1)

    def test_slave2(self):
        self.assertEqual(self.lnchr.case.status()[0], 1)

if __name__ == '__main__':
    unittest.main()