<script lang="ts">
	import { CheatingTable } from '$lib/components'
	import { findCheaters } from '$lib/services'
	import { cheaters } from '$lib/stores'
	import { FileDropzone } from '@skeletonlabs/skeleton'

	async function handleCsvUpload(e: Event) {
		const input = e.target as HTMLInputElement
		const files = input.files

		if (files) {
			const csvs: File[] = []
			for (const file of files) {
				if (file.type === 'text/csv') csvs.push(file)
			}
			const potentialCheaters = await findCheaters(csvs)
			cheaters.set(potentialCheaters)
		}
	}

	$: cheatingAmount = Object.keys($cheaters).length
</script>

{#if cheatingAmount < 1}
	<FileDropzone name="moodle-files-upload" multiple accept="text/csv" on:change={handleCsvUpload}>
		<svelte:fragment slot="message">
			<strong>Upload or drag and drop</strong> multiple Moodle CSVs
		</svelte:fragment>
	</FileDropzone>
{:else}
	<div class="max-h-full overflow-y-scroll">
		<CheatingTable data={$cheaters} />
	</div>
{/if}
