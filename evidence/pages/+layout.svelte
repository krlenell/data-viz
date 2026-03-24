<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	import { showQueries } from '@evidence-dev/component-utilities/stores';
	import { onMount } from 'svelte';
	export let data;

	onMount(() => {
		showQueries.set(false);
	});
</script>

<EvidenceDefaultLayout {data} neverShowQueries={true} homePageName="Dashboards">
	<slot slot="content" />
</EvidenceDefaultLayout>
