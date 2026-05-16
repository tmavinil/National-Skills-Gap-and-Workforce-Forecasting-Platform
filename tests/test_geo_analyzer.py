import unittest
from src.geo_analyzer import GeographicLaborAnalyzer

class TestGeographicLaborAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = GeographicLaborAnalyzer()

    def test_calculate_location_quotient_above_baseline(self):
        """
        Test that calculate_location_quotient correctly flags an LQ above 1.0 
        when regional concentration outperforms national baselines.
        """
        # Regional: 50 occupation workers out of 100 total local workers (0.5 ratio)
        # National: 200 occupation workers out of 1000 total national workers (0.2 ratio)
        # Expected LQ: 0.5 / 0.2 = 2.5
        local_occ_emp = 50
        total_local_emp = 100
        nat_occ_emp = 200
        total_nat_emp = 1000
        
        lq = self.analyzer.calculate_location_quotient(
            local_occ_emp, total_local_emp, nat_occ_emp, total_nat_emp
        )
        
        self.assertGreater(lq, 1.0)
        self.assertEqual(lq, 2.5)

    def test_calculate_location_quotient_zero_division_guards(self):
        """
        Test that calculate_location_quotient returns 0.0 for zero division scenarios.
        """
        # Test total_local_emp <= 0
        lq_local_emp_zero = self.analyzer.calculate_location_quotient(50, 0, 200, 1000)
        self.assertEqual(lq_local_emp_zero, 0.0)
        
        # Test total_nat_emp <= 0
        lq_nat_emp_zero = self.analyzer.calculate_location_quotient(50, 100, 200, 0)
        self.assertEqual(lq_nat_emp_zero, 0.0)
        
        # Test nat_occ_emp <= 0
        lq_nat_occ_zero = self.analyzer.calculate_location_quotient(50, 100, 0, 1000)
        self.assertEqual(lq_nat_occ_zero, 0.0)

if __name__ == '__main__':
    unittest.main()
