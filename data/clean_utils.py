def str_time_to_minutes(time_str: str) -> int:
	hour_strs = ["hour", "hours"]
	min_strs = ["min", "mins"]
	sec_strs = ["sec", "secs"]

	def count_occurance(orig_str: list[str], terms: list[str]) -> int:
		count = 0
		for term in terms:
			if term in split_str:
				count = int(orig_str[orig_str.index(term)-1])
		return count

	split_str = time_str.split(" ")

	hours = count_occurance(split_str, hour_strs)
	mins = count_occurance(split_str, min_strs)
	secs = count_occurance(split_str, sec_strs)

	total_mins = (hours * 60) + mins + (1 if secs >= 30 else 0)
	return total_mins


if __name__ == "__main__":
	test_1 = "57 mins 31 secs"
	test_2 = "1 hour 34 mins 35 secs"
	print(str_time_to_minutes(test_1))
	print(str_time_to_minutes(test_2))