<script>
	import Sidebar from "$lib/components/layout/Sidebar.svelte";
	import Header from "$lib/components/layout/Header.svelte";

	$: title = "Ayam Debugging";
</script>

<div class="d-flex flex-row min-vh-100">
	<!-- Main content area -->
	<div class="flex-grow-1 d-flex flex-column">
		<!-- Header -->
		<Header title={title}/>
		<!-- Page content -->
		<div class="flex-grow-1 p-4">
			<slot />
		</div>
	</div>
</div>
