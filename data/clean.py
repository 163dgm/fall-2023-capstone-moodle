import pandas as pd
import os
import clean_utils as utils

<<<<<<< HEAD
def clean():
	years = ["F20", "F21", "F22"]
=======
years = ["F20", "F21", "F22"]

def hw_clean():
	"""
	Takes each year's homework and removes unneeded columns, 
	removes each homework that was not finished, and converts
	string times to minutes.
	"""
>>>>>>> 109c1afaee86a63eca680864f14de55740a82742
	for year in years:
		hw_folder = sorted(os.listdir(f"./raw/{year}/HW"))
		for hw_path in hw_folder:
			raw_hw_path = f"./raw/{year}/HW/{hw_path}"
			raw_hw = pd.read_csv(raw_hw_path)

			# Remove unneeded columns
			removed_columns = ["Surname", "First name", "ID number", "Email address"]
			clean_hw = raw_hw.drop(columns=removed_columns)

			# Remove unfinished homework
			clean_hw = clean_hw.drop(clean_hw[clean_hw["State"] != "Finished"].index)

			# Convert string time taken to minutes
			clean_hw['Time taken'] = clean_hw['Time taken'].apply(utils.str_time_to_minutes)

			try:
				os.makedirs(f"./clean/{year}/HW/")
			except:
				None
			finally:
				clean_hw.to_csv(f"./clean/{year}/HW/{hw_path}", index=False)


if __name__ == "__main__":
	clean()