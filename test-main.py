import unittest
import csv
import os
import io
import sys
from tempfile import TemporaryDirectory
from main import combine_csv, search, report


class TestStockManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.csv1_path = os.path.join(self.temp_dir.name, "secteur1.csv")
        self.csv2_path = os.path.join(self.temp_dir.name, "secteur2.csv")

        csv1_content = [
            ["Produit", "quantité", "prix unitaire"],
            ["Clavier", "10", "15"],
            ["Souris", "5", "8"]
        ]
        csv2_content = [
            ["Produit", "quantité", "prix unitaire"],
            ["Ecran", "7", "120"],
            ["Clavier", "3", "15"]
        ]

        with open(self.csv1_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(csv1_content)

        with open(self.csv2_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(csv2_content)

        self.output_file = os.path.join(self.temp_dir.name, "fusion.csv")

        self.captured_output = io.StringIO()
        self.original_stdout = sys.stdout
        sys.stdout = self.captured_output

    def tearDown(self):
        sys.stdout = self.original_stdout
        self.temp_dir.cleanup()

    def test_combine_csv_creates_file(self):
        combine_csv(self.temp_dir.name, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_combine_csv_adds_secteur_column(self):
        combine_csv(self.temp_dir.name, self.output_file)
        with open(self.output_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assertIn("Secteur", reader.fieldnames)
            rows = list(reader)
            self.assertEqual(rows[0]["Secteur"], "secteur1")
            self.assertEqual(rows[-1]["Secteur"], "secteur2")

    def test_search_returns_results(self):
        combine_csv(self.temp_dir.name, self.output_file)
        search(self.output_file, "Clavier", field="Produit")
        output = self.captured_output.getvalue()
        self.assertIn("Clavier", output)

    def test_search_no_results(self):
        combine_csv(self.temp_dir.name, self.output_file)
        search(self.output_file, "NonExistant", field="Produit")
        output = self.captured_output.getvalue()
        self.assertIn("Aucun résultat trouvé", output)

    def test_report_calculation(self):
        combine_csv(self.temp_dir.name, self.output_file)

        temp_report_file = os.path.join(self.temp_dir.name, "report_test.csv")
        report(self.output_file, output_file=temp_report_file)

        with open(temp_report_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_qty = float(rows[0]["Quantity"])
            total_value = float(rows[0]["Total Value (€)"])

        self.assertEqual(total_qty, 25.0)
        self.assertEqual(total_value, 1075.0)


if __name__ == "__main__":
    unittest.main()
