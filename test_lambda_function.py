import unittest
import pandas as pd

from lambda_function import calculate_averages


class TestNutritionalAverages(unittest.TestCase):

    def test_calculate_averages(self):
        test_data = pd.DataFrame(
            {
                "Diet_type": ["vegan", "vegan", "keto", "keto"],
                "Protein(g)": [10, 20, 30, 50],
                "Carbs(g)": [100, 200, 20, 40],
                "Fat(g)": [5, 15, 40, 60],
            }
        )

        results = calculate_averages(test_data)

        vegan_result = next(
            result for result in results
            if result["Diet_type"] == "vegan"
        )

        keto_result = next(
            result for result in results
            if result["Diet_type"] == "keto"
        )

        self.assertEqual(vegan_result["Protein(g)"], 15.0)
        self.assertEqual(vegan_result["Carbs(g)"], 150.0)
        self.assertEqual(vegan_result["Fat(g)"], 10.0)

        self.assertEqual(keto_result["Protein(g)"], 40.0)
        self.assertEqual(keto_result["Carbs(g)"], 30.0)
        self.assertEqual(keto_result["Fat(g)"], 50.0)


if __name__ == "__main__":
    unittest.main()
