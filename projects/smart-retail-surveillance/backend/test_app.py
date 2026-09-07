import unittest

from app import summarize


class AnalyticsTests(unittest.TestCase):
    def test_summary_counts_categories_and_confidence(self):
        events = [
            {"class": "laptop", "confidence": "0.90"},
            {"class": "laptop", "confidence": "0.80"},
            {"class": "book", "confidence": "0.70"},
        ]
        result = summarize(events)
        self.assertEqual(result["total_events"], 3)
        self.assertEqual(result["unique_categories"], 2)
        self.assertEqual(result["categories"]["laptop"], 2)
        self.assertEqual(result["categories"]["book"], 1)
        self.assertAlmostEqual(result["average_confidence"], 0.8)


if __name__ == "__main__":
    unittest.main()
