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
                reader = csv.DictReader(in_csv, delimiter=';') # delimiter=";" car Excel sous Windows
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


def report(file, output_file=None):
    from datetime import date
    qte = 0
    valeur = 0

    if output_file is None:
        today_str = date.today().strftime("%Y-%m-%d")
        output_file = f"./rapport_stock_{today_str}.csv"

    with open(file, "r", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            try:
                qte += float(row["quantité"])
                valeur += float(row["quantité"]) * float(row["prix unitaire"])
            except ValueError:
                pass

    print(f"Quantité totale = {qte}")
    print(f"Valeur totale = {valeur} €")

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Quantity", "Total Value (€)"])
        writer.writerow([qte, valeur])

    print(f"Rapport généré : {output_file}")


if __name__ == '__main__':
    # Exemple de script à lancer :
    # python main.py --combine --input_dir ./script-perso-files --output_file fusion.csv
    # python main.py --search --search_file fusion.csv --field Secteur --value alimentaire

    parser = argparse.ArgumentParser(description="Outil de gestion des fichiers CSV de stocks")
    parser.add_argument("--combine", action="store_true", help="Fusionner tous les CSV d'un dossier en un seul fichier")
    parser.add_argument("--search", action="store_true", help="Rechercher dans un fichier CSV fusionné")
    parser.add_argument("--input_dir", type=str, help="Dossier contenant les fichiers CSV")
    parser.add_argument("--output_file", type=str, default="fichier_combine.csv", help="Nom du fichier fusionné")
    parser.add_argument("--search_file", type=str, help="Fichier CSV dans lequel effectuer la recherche")
    parser.add_argument("--field", type=str, help="Nom de la colonne où chercher")
    parser.add_argument("--value", type=str, help="Valeur à rechercher")

    args = parser.parse_args()

    if args.combine:
        if not args.input_dir:
            print("Erreur : --input_dir est requis pour --combine")
        else:
            combine_csv(args.input_dir, args.output_file)
            report(args.output_file)

    if args.search:
        if not args.search_file or not args.value:
            print("Erreur : --search_file et --value sont requis pour --search")
        else:
            search(args.search_file, args.value, args.field)