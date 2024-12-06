import unittest
import numpy as np
from frypto.volume import VolumeFeatures

class TestVolumeFeatures(unittest.TestCase):
    def setUp(self) -> None:
        """
        Setup common arrays for use in the test case.
        """
        self.close = np.array([100, 102, 101, 103, 105])
        self.volume = np.array([1000, 1500, 1200, 1300, 1600])

    def test_valid_input(self) -> None:
        """
        Test the VolumeFeatures class with valid input arrays
        """
        VF = VolumeFeatures(self.close, self.volume)
        df = VF.compute()
        columns = df.columns
        expected_columns = ['volume_change', 'OBV']

        # Verify the DataFrame contain the correct columns.
        for col in expected_columns:
            self.assertIn(col, columns)
        
        # Verify the content of the DataFrame
        np.testing.assert_array_almost_equal(df.volume_change, [0, 500, -300, 100, 300])
        np.testing.assert_array_almost_equal(df.OBV, [0, 1500, 300, 1600, 3200])

    def test_empty_input(self) -> None:
        """
        Test the VolumeFeatures class with empty input array.
        """
        with self.assertRaises(ValueError):
            VolumeFeatures(np.array([]), np.array([]))

if __name__ == "__main__":
    unittest.main()