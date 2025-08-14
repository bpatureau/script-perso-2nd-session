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
                reader = csv.DictReader(in_csv, delimiter=';') # Car je suis sur windows et Excel refuse d'utiliser la virgule dans mes fichiers CSV

                if writer is None:
                    fieldnames = reader.fieldnames + ["Secteur"]
                    writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
                    writer.writeheader()

                for row in reader:
                    row["Secteur"] = sector
                    writer.writerow(row)

    print(f"Consolidation terminée. Fichier généré : {output_file}")





if __name__ == '__main__':
    combine_csv("./script-perso-files", './script-perso-files-combined.csv')