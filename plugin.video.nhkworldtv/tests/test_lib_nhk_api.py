import unittest  # The test framework
import lib.nhk_api as nhk_api
import lib.utils as utils


class Test_Test_nhk_api(unittest.TestCase):

    # Test dynamically parsed API URL
    def test_nhk_api_ondemand_url(self):
        self.assertTrue(
            utils.get_url(nhk_api.rest_url['homepage_ondemand'],
                          False).status_code == 200)


if __name__ == '__main__':
    unittest.main()
