import csv
import os
import argparse
from pathlib import Path

def combine_csv(input_directory, output_file):
    files = list(Path(input_directory).glob('*.csv'))
    if not files:
        print("No files found")
        return

    with open(output_file, 'w', newline='', encoding="utf-8") as out_csv:
        writer = None
        for file in files:
            sector = file.stem
            with open(file, 'r', newline='', encoding="utf-8") as in_csv:
                reader = csv.DictReader(in_csv, delimiter=';') # delimiter=";" car je suis sur windows et Excel
                # utilise la virgule dans mes fichiers CSV.

                if writer is None:
                    fieldnames = reader.fieldnames + ["Secteur"]
                    writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
                    writer.writeheader()

                for row in reader:
                    row["Secteur"] = sector
                    writer.writerow(row)

    print(f"Consolidation terminée. Fichier généré : {output_file}")


def search(file, value, field=None):
    with open(file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        results = []

        for row in reader:
            if field:
                if field in row and value.lower() in str(row[field]).lower():
                    results.append(row)
            else:
                if any(value.lower() in str(v).lower() for v in row.values()):
                    results.append(row)

    if results:
        for r in results:
            print(r)
    else:
        print("Aucun résultat trouvé.")


def report(file):
    from datetime import date
    qte = 0
    value = 0
    today_str = date.today().strftime("%Y-%m-%d")
    output_file = f"./rapport_stock_{today_str}.csv"
    with open(file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            qte += int(row["quantité"])
            value += float(row["prix unitaire"])
        print("Quantité = " + str(qte))
        print("Prix unitaire total = " + str(value) + "€")
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";") # excel windows
            writer.writerow(["Quantity", "Value"])
            writer.writerow(["Quantity", qte])
            writer.writerow(["Totale Value (€)", value])

if __name__ == '__main__':
    report('./script-perso-files-combined.csv')
    # combine_csv("./script-perso-files", './script-perso-files-combined.csv')
    # search('./script-perso-files-combined.csv', 'alimentaire', 'Secteur')