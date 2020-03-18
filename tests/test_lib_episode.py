import unittest   # The test framework
from lib.episode import Episode
from datetime import datetime


class Test_Test_Episode(unittest.TestCase):

    _now = datetime.now

    def test_create_episode(self):
        episode = Episode()
        self.assertIsNotNone(episode)

   
if __name__ == '__main__':
    unittest.main()
