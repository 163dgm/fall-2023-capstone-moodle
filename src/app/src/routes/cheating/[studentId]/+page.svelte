<script lang="ts">
	import { page } from '$app/stores'
	import { StudentCheatingTable } from '$lib/components'
	import { cheaters } from '$lib/stores'

	const studentId = $page.params.studentId
</script>

<StudentCheatingTable data={$cheaters[parseInt(studentId)]} />
