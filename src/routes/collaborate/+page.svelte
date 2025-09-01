<script>
    import CollaboratePage from "$lib/components/collaborate/CollaboratePage.svelte";
    
    export let data;
</script>

<CollaboratePage initialIdeas={data.ideas} />
