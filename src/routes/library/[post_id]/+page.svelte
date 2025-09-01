<script>
    import IndividualPost from "$lib/components/library/IndividualPost.svelte";
    import { page } from '$app/stores';

    $: postId = $page.params.post_id;
</script>

<IndividualPost {postId} />
