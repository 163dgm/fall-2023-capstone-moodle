import os
import pandas as pd
import clean_utils as utils

years = ["F20", "F21", "F22"]


def clean(assgn: str):
    """
    Takes each year's homework and removes unneeded columns,
    removes each homework that was not finished, and converts
    string times to minutes.
    """
    for year in years:
        assgn_folder = None
        try:
            assgn_folder = sorted(os.listdir(f"../raw/{year}/{assgn}"))
        except:
            continue

        for assgn_path in assgn_folder:
            raw_assgn_path = f"../raw/{year}/{assgn}/{assgn_path}"
            raw_assgn = pd.read_csv(raw_assgn_path)

            # Remove unneeded columns
            removed_columns = ["Surname", "First name", "Email address"]
            clean_assgn = raw_assgn.drop(columns=removed_columns)

            # Remove unfinished homework
            clean_assgn = clean_assgn.drop(
                clean_assgn[clean_assgn["State"] != "Finished"].index
            )

            # Convert string time taken to minutes
            clean_assgn["Time taken"] = clean_assgn["Time taken"].apply(
                utils.str_time_to_minutes
            )

            try:
                os.makedirs(f"./{year}/{assgn}/")
            except:
                None
            finally:
                clean_assgn.to_csv(f"./{year}/{assgn}/{assgn_path}", index=False)


def xlsx_clean():
    """
    Splits `../raw/Moodle Datasets.xlsx` into individual sheets
    and moves them into each respective year's folder.
    """
    for year in years:
        year_sheet = pd.read_excel("../raw/Moodle Datasets.xlsx", sheet_name=year)
        year_sheet.to_csv(f"./{year}/deadlines.csv", index=False)


if __name__ == "__main__":
    pass
