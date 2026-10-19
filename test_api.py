import unittest

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


class TestApi(unittest.TestCase):
    def test_dashboard_is_served(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Trading Risk Analytics", response.text)

    def test_summary_fields(self):
        body = client.get("/summary").json()
        for key in ("annualized_volatility", "var_95", "var_99", "max_drawdown"):
            self.assertIn(key, body)
        self.assertGreater(body["annualized_volatility"], 0)
        self.assertLessEqual(body["max_drawdown"], 0)
        self.assertGreaterEqual(body["var_99"], body["var_95"])

    def test_var_endpoint(self):
        body = client.get("/var", params={"confidence": 0.9}).json()
        self.assertEqual(body["confidence"], 0.9)
        self.assertGreaterEqual(body["var"], 0)

    def test_var_rejects_bad_confidence(self):
        for bad in (0, 1, 1.5, -0.2):
            response = client.get("/var", params={"confidence": bad})
            self.assertEqual(response.status_code, 422)

    def test_value_series(self):
        body = client.get("/portfolio/value").json()
        self.assertEqual(len(body), 500)
        self.assertIn("date", body[0])

    def test_drawdown_never_positive(self):
        body = client.get("/portfolio/drawdown").json()
        self.assertTrue(all(row["drawdown"] <= 0 for row in body))

    def test_holdings_weights_sum_to_one(self):
        body = client.get("/holdings").json()
        self.assertEqual(len(body), 5)
        self.assertAlmostEqual(sum(row["weight"] for row in body), 1.0)


if __name__ == "__main__":
    unittest.main()
