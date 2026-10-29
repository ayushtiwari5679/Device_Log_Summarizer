import unittest
from src.cleaning import clean_sensor_readings


class CleanSensorReadingsTests(unittest.TestCase):
    def test_converts_filters_and_clips(self):
        self.assertEqual(
            clean_sensor_readings([12, "3.5", None, "bad", -2, 700, 500]),
            [12.0, 3.5, 500.0, 500.0],
        )

    def test_empty_and_all_invalid(self):
        self.assertEqual(clean_sensor_readings([]), [])
        self.assertEqual(clean_sensor_readings([None, "x", -1]), [])

    def test_ignores_non_finite_values(self):
        self.assertEqual(clean_sensor_readings(["nan", "inf", "-inf", 4]), [4.0])


if __name__ == "__main__":
    unittest.main()
