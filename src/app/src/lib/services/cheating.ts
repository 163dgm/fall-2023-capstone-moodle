import type { CheatingResults, Assignment } from '$lib/types'
import { fromCSV, DataFrame } from 'data-forge'

export async function findCheaters(csvs: File[]) {
	const repeatOffenders: CheatingResults = {}
	for (const csv of csvs) {
		const df = fromCSV(await csv.text())

		const outliers = findOutliers(df)
		for (const outlier of outliers) {
			const id = parseInt(outlier['ID number'])
			const student = repeatOffenders[id]
			if (student) {
				student.cheatCount += 1
				student.assignments.push(outlier)
			} else {
				repeatOffenders[id] = {
					cheatCount: 1,
					assignments: [outlier]
				}
			}
		}
	}

	return repeatOffenders
}

function findOutliers(df: DataFrame) {
	const timeCol = df.getSeries('Time taken').parseFloats()
	const mean = timeCol.mean()
	const std = timeCol.std()

	const susTime = mean - std
	const susGrade = 18

	const outliers: Assignment[] = []
	df.forEach((row: Assignment) => {
		if (Number(row['Time taken']) < susTime && Number(row['Grade/20.00']) > susGrade) {
			outliers.push(row)
		}
	})

	return outliers
}

/*
def find_potential_cheaters(df: pd.DataFrame) -> pd.DataFrame:
    outliers = pd.DataFrame()
    time_col = df["Time taken"]

    desc = time_col.describe()
    # IQR lower bound was returning negative numbers so it was inaccurate, instead
    # we check if the time taken was two standard deviations from the mean
    mean = desc["mean"]
    std = desc["std"]

    # Select all columns where the time was less than 1 standard dev from mean
    outliers = df[time_col < (mean - (1 * std))]

    return outliers[outliers["Grade/20.00"] > 18]

*/
