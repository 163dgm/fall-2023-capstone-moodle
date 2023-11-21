<script lang="ts" context="module">
	import { page } from '$app/stores'
	import '../app.css'
</script>

<script lang="ts">
	import { AppBar, AppRail, AppRailAnchor, AppShell } from '@skeletonlabs/skeleton'
</script>

<AppShell regionPage="relative" slotPageHeader="sticky top-0 z-10" slotPageContent="p-8">
	<svelte:fragment slot="header">
		<AppBar shadow="shadow-xl">
			<a class="font-medium text-xl" href="/">Moodle Buddy</a>
		</AppBar>
	</svelte:fragment>
	<svelte:fragment slot="sidebarLeft">
		<AppRail>
			<AppRailAnchor
				href="/struggling"
				title="Struggling"
				selected={$page.url.pathname.includes('struggling')}
			>
				<svelte:fragment slot="lead">😰</svelte:fragment>
				<span>Find Struggling Students</span>
			</AppRailAnchor>
			<AppRailAnchor
				href="/cheating"
				title="Cheating"
				selected={$page.url.pathname.includes('cheating')}
			>
				<svelte:fragment slot="lead">😈</svelte:fragment>
				<span>Detect Cheating</span>
			</AppRailAnchor>
			<AppRailAnchor href="/idk" title="idk" selected={$page.url.pathname.includes('idk')}>
				<svelte:fragment slot="lead">??</svelte:fragment>
				<span>Something</span>
			</AppRailAnchor>
		</AppRail>
	</svelte:fragment>
	<slot />
</AppShell>
