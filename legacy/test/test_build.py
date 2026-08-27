import unittest
import tomoe

class TestVersion(unittest.TestCase):

    def test_version(self):
        print(tomoe.__version__)
        self.assertIsInstance(tomoe.__version__, str)
        self.assertRegex(tomoe.__version__, r"^\d+\.\d+\.\d+$")  # contoh: 1.0.0

if __name__ == "__main__":
    unittest.main()
