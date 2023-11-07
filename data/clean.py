import pandas as pd
import os

def clean():
	years = ["F20", "F21", "F22"]
	for year in years:
		hw_folder = sorted(os.listdir(f"./raw/{year}/HW"))
		for hw_path in hw_folder:
			raw_hw_path = f"./raw/{year}/HW/{hw_path}"
			raw_hw = pd.read_csv(raw_hw_path)
			removed_columns = ["Surname", "First name", "ID number", "Email address"]
			clean_hw = raw_hw.drop(columns=removed_columns)
			clean_hw = clean_hw.drop(clean_hw[clean_hw["State"] != "Finished"].index)

			try:
				os.makedirs(f"./clean/{year}/HW/")
			except:
				None
			finally:
				clean_hw.to_csv(f"./clean/{year}/HW/{hw_path}", index=False)


if __name__ == "__main__":
	clean()