import csv
from typing import Tuple, Optional, NoReturn
from pathlib import Path

def csv_converter(
    input_file: str = "./data/markets.csv",
    output_file: str = "./data/markets_converted.csv",
    input_format: Tuple[str, str] = (",", ";"),
    output_format: Tuple[str, str] = ("|", ","),
) -> Optional[NoReturn]:
    
    if not all(sep and isinstance(sep, str) for sep in [*input_format, *output_format]):
        raise ValueError("Les séparateurs doivent être des chaînes non vides.")

    if not Path(input_file).is_file():
        raise FileNotFoundError(f"Fichier introuvable : {input_file}")

    try:
        with open(input_file, "r", newline="", encoding="utf-8") as infile, \
             open(output_file, "w", newline="", encoding="utf-8") as outfile:

            reader = csv.reader(infile, sep=input_format[0])
            writer = csv.writer(outfile, sep=output_format[0], quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                new_row = [cell.replace(input_format[1], output_format[1]) for cell in row]
                writer.writerow(new_row)

        print(f"✅ Conversion réussie : {output_file}")

    except csv.Error as e:
        raise csv.Error(f"Erreur CSV ligne {reader.line_num}: {str(e)}")
    
    except Exception as e:
        raise RuntimeError(f"Erreur inattendue : {str(e)}")

if __name__ == "__main__":
    try:
        csv_converter()  

    except Exception as e:
        print(f"❌ Échec : {str(e)}")