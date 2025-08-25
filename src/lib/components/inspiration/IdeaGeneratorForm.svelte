<script>
    import GeneratedIdeaCard from "./GeneratedIdeaCard.svelte";

    /**
     * @typedef {Object} GeneratedIdea
     * @property {string} title
     * @property {string} description
     * @property {string[]} [tags]
     * @property {string} [intent]
     */

    let keyword = "";
    let tone = "";
    let audience = "General";
    let formality = "Neutral";
    let domain = "General";
    let intent = "Inform";
    /** @type {GeneratedIdea[]} */
    let generatedIdeas = [];

    function generateIdeas() {
        // Simulate API call with mock ideas
        generatedIdeas = [
            {
                title: "How to Boost Engagement on Social Media",
                description:
                    "Tips and strategies for increasing audience interaction and reach.",
                tags: ["Social Media", "Engagement"],
                intent,
            },
            {
                title: "Creative Content Ideas for Marketing",
                description:
                    "Unique approaches to content creation for marketing campaigns.",
                tags: ["Marketing", "Content Creation"],
                intent,
            },
            {
                title: "Latest Trends in Digital Content",
                description:
                    "An overview of what's trending in digital content this month.",
                tags: ["Trends", "Digital"],
                intent,
            },
        ];
    }
</script>

<div class="mb-4">
    <h2>AI Idea Generator</h2>
    <label class="form-label" for="keywordInput">Topic/Keyword</label>
    <input
        id="keywordInput"
        class="form-control mb-2"
        placeholder="Enter topic/keyword"
        bind:value={keyword}
    />
    <label class="form-label" for="toneInput">Tone</label>
    <input
        id="toneInput"
        class="form-control mb-2"
        placeholder="Tone"
        bind:value={tone}
    />

    <!-- Audience Toggle Group -->
    <div class="row align-items-center mt-3 mb-2">
        <div class="col-2">
            <label class="form-label mb-0">Audience:</label>
        </div>
        <div class="col">
            <div class="toggle-group">
                {#each ["General", "Knowledgeable", "Expert"] as option}
                    <button
                        class="toggle-btn me-2"
                        class:active={audience === option}
                        type="button"
                        on:click={() => (audience = option)}>{option}</button
                    >
                {/each}
            </div>
        </div>
    </div>

    <!-- Formality Toggle Group -->
    <div class="row align-items-center mt-3 mb-2">
        <div class="col-2">
            <label class="form-label mb-0">Formality:</label>
        </div>
        <div class="col">
            <div class="toggle-group">
                {#each ["Informal", "Neutral", "Formal"] as option}
                    <button
                        class="toggle-btn me-2"
                        class:active={formality === option}
                        type="button"
                        on:click={() => (formality = option)}>{option}</button
                    >
                {/each}
            </div>
        </div>
    </div>

    <!-- Domain Toggle Group -->
    <div class="row align-items-center mt-3 mb-2">
        <div class="col-2">
            <label class="form-label mb-0">Domain:</label>
        </div>
        <div class="col">
            <div class="toggle-group">
                {#each ["Marketing", "Social Media", "Content Creation", "Trends"] as option}
                    <button
                        class="toggle-btn me-2"
                        class:active={domain === option}
                        type="button"
                        on:click={() => (domain = option)}>{option}</button
                    >
                {/each}
            </div>
        </div>
    </div>

    <!-- Intent Toggle Group -->
    <div class="row align-items-center mt-3 mb-2">
        <div class="col-2">
            <label class="form-label mb-0">Intent:</label>
        </div>
        <div class="col">
            <div class="toggle-group">
                {#each ["Inform", "Describe", "Convince", "Tell A Story"] as option}
                    <button
                        class="toggle-btn me-2"
                        class:active={intent === option}
                        type="button"
                        on:click={() => (intent = option)}>{option}</button
                    >
                {/each}
            </div>
        </div>
    </div>

    <button class="btn btn-primary mt-2" type="button" on:click={generateIdeas}>
        Generate Ideas
    </button>

    {#if generatedIdeas.length}
        <div class="mt-4">
            <h3>Generated Ideas</h3>
            <div class="row">
                {#each generatedIdeas as idea}
                    <div class="col-md-4">
                        <GeneratedIdeaCard {idea} />
                    </div>
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .toggle-btn {
        background: #f5f5fa;
        color: #222;
        border: 1px solid #d6d6e7;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        font-weight: 500;
        transition:
            background 0.2s,
            color 0.2s;
    }
    .toggle-btn.active,
    .toggle-btn:active {
        background: #7c3aed; /* violet */
        color: #fff;
        border-color: #7c3aed;
    }
    .toggle-btn:hover {
        background: #ede9fe;
        color: #222;
    }
</style>
