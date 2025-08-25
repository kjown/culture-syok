<script>
    export let idea;
</script>

<div class="card h-100 mb-3">
    <div class="card-body">
        <h5 class="card-title">{idea.title}</h5>
        <p class="card-text">{idea.description}</p>
        {#if idea.tags}
            <div class="mt-2">
                {#each idea.tags as tag}
                    <span class="badge bg-secondary me-1">{tag}</span>
                {/each}
            </div>
        {/if}
        {#if idea.intent}
            <div class="mt-2 small text-muted">Intent: {idea.intent}</div>
        {/if}
    </div>
</div>