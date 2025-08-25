<script>
    import GeneratedIdeaCard from "./GeneratedIdeaCard.svelte";

    /**
     * @typedef {Object} IdeaItem
     * @property {string} title
     * @property {string} description
     * @property {string[]} tags
     * @property {string} intent
     */

    /** @type {Record<string, IdeaItem[]>} */
    const ideas = {
        "New Ideas": [
            {
                title: "Repurpose Blog Posts for Social Media",
                description:
                    "Turn your old blog posts into engaging social media content.",
                tags: ["Content Creation", "Social Media"],
                intent: "Inform",
            },
            {
                title: "Weekly Marketing Tip",
                description:
                    "Share a quick marketing tip every week to boost engagement.",
                tags: ["Marketing", "Tips"],
                intent: "Describe",
            },
        ],
        Drafting: [
            {
                title: "Draft: Instagram Carousel on Trends",
                description: "A carousel post about the latest digital trends.",
                tags: ["Social Media", "Trends"],
                intent: "Tell A Story",
            },
        ],
        "Ready to Schedule": [
            {
                title: "Scheduled: Email Newsletter",
                description:
                    "Monthly newsletter ready to be sent to subscribers.",
                tags: ["Email", "Newsletter"],
                intent: "Inform",
            },
        ],
    };

    let activeTab = "New Ideas";
    let tabs = Object.keys(ideas);
</script>

<div class="mb-4">
    <h2 class="mb-3">Idea Board</h2>
    <ul class="nav nav-tabs mb-3">
        {#each tabs as tab}
            <li class="nav-item">
                <button
                    class="nav-link {activeTab === tab ? 'active' : ''}"
                    type="button"
                    on:click={() => (activeTab = tab)}
                >
                    {tab}
                </button>
            </li>
        {/each}
    </ul>
    <div>
        {#each ideas[activeTab] as idea}
            <GeneratedIdeaCard {idea} />
        {/each}
        {#if ideas[activeTab].length === 0}
            <div class="text-muted py-4">No ideas in this category yet.</div>
        {/if}
    </div>
</div>

<style>
    .nav-tabs .nav-link {
        border: none;
        background: transparent;
        color: #222;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        border-bottom: 2px solid transparent;
        transition:
            color 0.2s,
            border-color 0.2s;
    }
    .nav-tabs .nav-link.active {
        color: #2563eb;
        border-bottom: 2px solid #2563eb;
        background: #f8fafc;
    }
</style>
