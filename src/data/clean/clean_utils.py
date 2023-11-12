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

	total_mins = (hours * 60) + mins + (secs / 60)
	return round(total_mins, 2)


if __name__ == "__main__":
	times = ["57 mins 31 secs", "1 hour 34 mins 35 secs", "2 hours"]
	for time in times:
		print(time, ":", str_time_to_minutes(time))
		
		