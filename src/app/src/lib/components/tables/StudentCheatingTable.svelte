<script lang="ts">
	import type { CheatingResults } from '$lib/services/cheating'
	import { Table, tableMapperValues, type TableSource } from '@skeletonlabs/skeleton'

	export let data: CheatingResults[number]

	const tableData = data.assignments.map((assgn) => {
		return {
			name: 'Assignment Name',
			grade: assgn['Grade/20.00'],
			timeTaken: assgn['Time taken']
		}
	})

	const cheatingTable: TableSource = {
		head: ['Assignment Name', 'Grade/20', 'Time Taken'],
		body: tableMapperValues(tableData, ['name', 'grade', 'timeTaken'])
	}
</script>

<Table source={cheatingTable} />
