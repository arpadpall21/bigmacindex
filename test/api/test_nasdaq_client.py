import sys
import os
sys.path.append(os.getcwd())

from unittest import TestCase
from unittest.mock import Mock, patch
from parameterized import parameterized
from datetime import datetime

from  api.nasdaq_client import NasdaqClient


# runned out of time so I couldn't figure out how mocking works in Python (done this with Jest JavaScript but that's different here sorry)

class TestNasdaqClient(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = "_X8Mn1-mJaoR7Qi7qiqf"
        cls.client = NasdaqClient(api_key)

    @parameterized.expand([
        ("hungary_test", "Hungary", datetime(2021, 1, 31), -46.5),
        ("russia_test", "Russia", datetime(2021, 1, 31), -68.0),
        ("chile_test", "Chile", datetime(2021, 1, 31), -27.8),
        ("mexico_test", "Mexico", datetime(2021, 1, 31), -52.6),
    ])
    def test_the_results(self, name, country, date, expectation):
        actual = self.client.get_bigmac_index_as_of(date, country)
        self.assertAlmostEqual(actual, expectation, msg=f"Test failed for {country} as of {date}")
