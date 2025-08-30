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

<div class="idea-generator">
    <div class="generator-header">
        <div class="header-icon">
            <i class="fas fa-magic"></i>
        </div>
        <div>
            <h2 class="generator-title">AI Idea Generator</h2>
            <p class="generator-subtitle">Generate creative content ideas powered by artificial intelligence</p>
        </div>
    </div>

    <form class="generator-form">
        <!-- Input Fields -->
        <div class="input-grid">
            <div class="form-section">
                <label class="form-label" for="keywordInput">
                    <i class="fas fa-hashtag me-2"></i>
                    Topic/Keyword
                </label>
                <input
                    id="keywordInput"
                    class="form-control"
                    placeholder="Enter your main topic or keyword..."
                    bind:value={keyword}
                />
            </div>
            <div class="form-section">
                <label class="form-label" for="toneInput">
                    <i class="fas fa-palette me-2"></i>
                    Tone
                </label>
                <input
                    id="toneInput"
                    class="form-control"
                    placeholder="e.g., Professional, Casual, Humorous..."
                    bind:value={tone}
                />
            </div>
        </div>

        <!-- Toggle Groups -->
        <div class="toggle-sections">
            <!-- Audience Toggle Group -->
            <div class="toggle-section">
                <label class="section-label">
                    <i class="fas fa-users me-2"></i>
                    Target Audience
                </label>
                <div class="toggle-group">
                    {#each ["General", "Knowledgeable", "Expert"] as option}
                        <button
                            class="toggle-btn"
                            class:active={audience === option}
                            type="button"
                            on:click={() => (audience = option)}
                        >
                            {option}
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Formality Toggle Group -->
            <div class="toggle-section">
                <label class="section-label">
                    <i class="fas fa-balance-scale me-2"></i>
                    Formality Level
                </label>
                <div class="toggle-group">
                    {#each ["Informal", "Neutral", "Formal"] as option}
                        <button
                            class="toggle-btn"
                            class:active={formality === option}
                            type="button"
                            on:click={() => (formality = option)}
                        >
                            {option}
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Domain Toggle Group -->
            <div class="toggle-section">
                <label class="section-label">
                    <i class="fas fa-industry me-2"></i>
                    Content Domain
                </label>
                <div class="toggle-group">
                    {#each ["Marketing", "Social Media", "Content Creation", "Trends"] as option}
                        <button
                            class="toggle-btn"
                            class:active={domain === option}
                            type="button"
                            on:click={() => (domain = option)}
                        >
                            {option}
                        </button>
                    {/each}
                </div>
            </div>

            <!-- Intent Toggle Group -->
            <div class="toggle-section">
                <label class="section-label">
                    <i class="fas fa-bullseye me-2"></i>
                    Content Intent
                </label>
                <div class="toggle-group">
                    {#each ["Inform", "Describe", "Convince", "Tell A Story"] as option}
                        <button
                            class="toggle-btn"
                            class:active={intent === option}
                            type="button"
                            on:click={() => (intent = option)}
                        >
                            {option}
                        </button>
                    {/each}
                </div>
            </div>
        </div>

        <!-- Generate Button -->
        <div class="generate-section">
            <button class="btn-generate" type="button" on:click={generateIdeas}>
                <i class="fas fa-sparkles me-2"></i>
                Generate Creative Ideas
            </button>
        </div>
    </form>

    <!-- Generated Ideas -->
    {#if generatedIdeas.length}
        <div class="generated-ideas">
            <div class="ideas-header">
                <h3 class="ideas-title">
                    <i class="fas fa-lightbulb me-2"></i>
                    Generated Ideas
                </h3>
                <p class="ideas-subtitle">Fresh content ideas based on your preferences</p>
            </div>
            <div class="ideas-grid">
                {#each generatedIdeas as idea}
                    <GeneratedIdeaCard {idea} />
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .idea-generator {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin-bottom: 2rem;
    }

    .generator-header {
        padding: 2rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .header-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
    }

    .generator-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .generator-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .generator-form {
        padding: 2rem;
    }

    .input-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .form-section {
        margin-bottom: 1rem;
    }

    .form-label {
        display: flex;
        align-items: center;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
    }

    .form-label i {
        color: #667eea;
    }

    .form-control {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
        width: 100%;
    }

    .form-control:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
        background: rgba(255, 255, 255, 0.95);
    }

    .toggle-sections {
        display: grid;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .toggle-section {
        background: rgba(102, 126, 234, 0.02);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .section-label {
        display: flex;
        align-items: center;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        font-size: 1rem;
    }

    .section-label i {
        color: #667eea;
    }

    .toggle-group {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
    }

    .toggle-btn {
        background: rgba(255, 255, 255, 0.8);
        color: #4a5568;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1.25rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
        backdrop-filter: blur(10px);
    }

    .toggle-btn:hover {
        background: rgba(102, 126, 234, 0.05);
        border-color: #667eea;
        color: #2d3748;
        transform: translateY(-1px);
    }

    .toggle-btn.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .generate-section {
        text-align: center;
        padding-top: 1rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }

    .btn-generate {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0 auto;
    }

    .btn-generate:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .generated-ideas {
        padding: 2rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
        background: rgba(102, 126, 234, 0.02);
    }

    .ideas-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .ideas-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .ideas-title i {
        color: #667eea;
    }

    .ideas-subtitle {
        color: #718096;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
    }

    .ideas-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .generator-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            text-align: center;
        }

        .generator-form {
            padding: 1.5rem 1rem;
        }

        .input-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .toggle-section {
            padding: 1rem;
        }

        .toggle-group {
            gap: 0.5rem;
        }

        .toggle-btn {
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
        }

        .btn-generate {
            width: 100%;
            justify-content: center;
            padding: 0.875rem 1.5rem;
        }

        .ideas-grid {
            grid-template-columns: 1fr;
        }

        .generated-ideas {
            padding: 1.5rem 1rem;
        }
    }
</style>
