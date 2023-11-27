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
				href="/performance"
				title="Performance"
				selected={$page.url.pathname.includes('performance')}
			>
				<svelte:fragment slot="lead">
					<!-- Heroicons/solid: chart-bar -->
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="w-6 h-6"
					>
						<path
							d="M18.375 2.25c-1.035 0-1.875.84-1.875 1.875v15.75c0 1.035.84 1.875 1.875 1.875h.75c1.035 0 1.875-.84 1.875-1.875V4.125c0-1.036-.84-1.875-1.875-1.875h-.75zM9.75 8.625c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v11.25c0 1.035-.84 1.875-1.875 1.875h-.75a1.875 1.875 0 01-1.875-1.875V8.625zM3 13.125c0-1.036.84-1.875 1.875-1.875h.75c1.036 0 1.875.84 1.875 1.875v6.75c0 1.035-.84 1.875-1.875 1.875h-.75A1.875 1.875 0 013 19.875v-6.75z"
						/>
					</svg>
				</svelte:fragment>
				<span>Performance</span>
			</AppRailAnchor>
			<AppRailAnchor
				href="/cheating"
				title="Cheating"
				selected={$page.url.pathname.includes('cheating')}
			>
				<svelte:fragment slot="lead">
					<!-- Heroicons/solid: exclamation-triangle -->
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 24 24"
						fill="currentColor"
						class="w-6 h-6"
					>
						<path
							fill-rule="evenodd"
							d="M9.401 3.003c1.155-2 4.043-2 5.197 0l7.355 12.748c1.154 2-.29 4.5-2.599 4.5H4.645c-2.309 0-3.752-2.5-2.598-4.5L9.4 3.003zM12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75zm0 8.25a.75.75 0 100-1.5.75.75 0 000 1.5z"
							clip-rule="evenodd"
						/>
					</svg>
				</svelte:fragment>
				<span>Cheating</span>
			</AppRailAnchor>
			<AppRailAnchor href="/idk" title="idk" selected={$page.url.pathname.includes('idk')}>
				<svelte:fragment slot="lead">??</svelte:fragment>
				<span>Something</span>
			</AppRailAnchor>
		</AppRail>
	</svelte:fragment>
	<slot />
</AppShell>
