import unittest
from utils.location import round_coordinates

class TestLocation(unittest.TestCase):
    def test_round_coordinates(self):
        """Test coordinate rounding functionality"""
        # Test cases with different precisions
        test_cases = [
            ((55.7558, 37.6173), (55.7558, 37.6173)),  # Moscow coordinates
            ((51.50722, -0.12750), (51.5072, -0.1275)),  # London coordinates
            ((40.7127753, -74.0059728), (40.7128, -74.0060)),  # New York coordinates
        ]
        
        for (input_lat, input_lon), (expected_lat, expected_lon) in test_cases:
            rounded_lat, rounded_lon = round_coordinates(input_lat, input_lon)
            self.assertEqual(rounded_lat, expected_lat, f"Latitude rounding failed for {input_lat}")
            self.assertEqual(rounded_lon, expected_lon, f"Longitude rounding failed for {input_lon}")

if __name__ == '__main__':
    unittest.main() 