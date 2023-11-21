<script lang="ts">
	import { goto } from '$app/navigation'
	import type { CheatingResults } from '$lib'
	import { Table, tableMapperValues, type TableSource } from '@skeletonlabs/skeleton'

	export let data: CheatingResults

	const tableData = Object.entries(data).map(([id, data]) => {
		return {
			id,
			first: 'John',
			last: 'Smith',
			cheatCount: data.cheatCount,
			assignments: data.assignments
		}
	})

	const cheatingTable: TableSource = {
		head: ['ID Number', 'First Name', 'Last Name', 'Assignments Flagged'],
		body: tableMapperValues(tableData, ['id', 'first', 'last', 'cheatCount']),
		meta: tableMapperValues(tableData, ['id', 'first', 'last', 'cheatCount', 'assignments']),
		foot: [
			'<span class="font-bold">Total Students Flagged</span>',
			'',
			'',
			`<span class="badge variant-filled-primary">${tableData.length} Students</span>`
		]
	}

	async function handleTableSelect(e: CustomEvent<string[]>) {
		await goto('/cheating/' + e.detail[0])
	}
</script>

<Table
	source={cheatingTable}
	interactive
	on:selected={handleTableSelect}
	regionHead="sticky top-0 z-10"
/>
