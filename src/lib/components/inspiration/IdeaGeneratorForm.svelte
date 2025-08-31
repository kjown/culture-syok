<script>
    import GeneratedIdeaCard from "./GeneratedIdeaCard.svelte";
    import { createEventDispatcher, onMount } from 'svelte';

    const dispatch = createEventDispatcher();

    /**
     * @typedef {Object} GeneratedIdea
     * @property {string} title
     * @property {string} description
     * @property {string[]} [tags]
     * @property {string} [intent]
     */

    let keyword = "";
    // let tone = "";
    let audience = "General";
    let formality = "Neutral";
    let domain = "General";
    let intent = "Inform";
    /** @type {GeneratedIdea[]} */
    let generatedIdeas = [];

    /** @type {any[]} */
    let availableTrends = [];
    /** @type {any | null} */
    let selectedTrend = null;
    let loadingTrends = true;
    let isGenerating = false;

    // Form fields matching your PlanRequest model
    let product = '';
    let objective = '';
    let call_to_action = '';
    let content_medium = 'Instagram Reel';
    let tone = 'Informal and Fun';

    const contentMediums = [
        'Instagram Post',
        'Instagram Reel',
        'TikTok Video',
        'Facebook Post',
        'Twitter Thread',
        'Blog Post',
        'LinkedIn Article'
    ];

    const tones = [
        'Professional',
        'Casual',
        'Informal and Fun',
        'Educational',
        'Inspirational',
        'Humorous'
    ];

    // 1. Fetch trends from your Python backend on component mount
    onMount(async () => {
        try {
            // NOTE: Ensure your FastAPI server is running on port 8000
            const response = await fetch('http://127.0.0.1:8000/api/get-trends');
            if (response.ok) {
                const data = await response.json();
                availableTrends = data.trends || [];
            } else {
                console.error('Failed to fetch trends:', response.status);
                alert('Could not load trends from the backend. Please ensure the server is running.');
            }
        } catch (error) {
            console.error('Error fetching trends:', error);
            alert('Could not connect to the backend. Please ensure the server is running.');
        } finally {
            loadingTrends = false;
        }
    });

    /** @param {any} trend */
    function handleSelectTrend(trend) {
        selectedTrend = trend;
    }

    // 2. Generate the content plan
    async function generatePlan() {
        if (!selectedTrend || !product || !objective) {
            alert('Please select a trend and fill out all required fields.');
            return;
        }

        isGenerating = true;
        dispatch('loading');

        try {
            const requestBody = {
                trend: selectedTrend,
                product,
                objective,
                call_to_action,
                content_medium,
                tone
            };

            const response = await fetch('http://127.0.0.1:8000/api/generate-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestBody)
            });

            if (response.ok) {
                const planData = await response.json();
                dispatch('planGenerated', planData);
            } else {
                const errorData = await response.json();
                console.error('Plan generation failed:', errorData);
                alert('Failed to generate content plan. Please try again.');
            }
        } catch (error) {
            console.error('Error generating plan:', error);
            alert('Error generating plan. Please check your connection.');
        } finally {
            isGenerating = false;
        }
    }

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

<div class="idea-generator-container">
    <div class="row">
        <!-- Trends Selection Column -->
        <div class="col-lg-4">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">1. Select a Trend</h5>
                </div>
                <div class="card-body">
                    {#if loadingTrends}
                        <div class="text-center py-4">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-2 text-muted small">Analyzing latest trends...</p>
                        </div>
                    {:else if availableTrends.length > 0}
                        <div class="trends-list">
                            {#each availableTrends as trend (trend.trend_name)}
                                <div
                                    class="trend-item p-3 mb-2 rounded border"
                                    class:active={selectedTrend?.trend_name === trend.trend_name}
                                    on:click={() => handleSelectTrend(trend)}
                                    on:keydown={(e) => e.key === 'Enter' && handleSelectTrend(trend)}
                                    role="button"
                                    tabindex="0"
                                >
                                    <h6 class="mb-1">{trend.trend_name}</h6>
                                    <p class="small text-muted mb-2">{trend.description}</p>
                                    {#if trend.representative_image_url}
                                        <img
                                            src={trend.representative_image_url}
                                            alt={trend.trend_name}
                                            class="img-fluid rounded mt-1"
                                        />
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    {:else}
                        <p class="text-muted">No trends available. Please try again later.</p>
                    {/if}
                </div>
            </div>
        </div>

        <!-- Content Plan Form Column -->
        <div class="col-lg-8">
            <div class="card mb-4">
                <div class="card-header">
                    <h5 class="mb-0">2. Generate Content Plan</h5>
                </div>
                <div class="card-body">
                    {#if !selectedTrend}
                        <div class="text-center text-muted p-5">
                            <i class="fas fa-arrow-left fa-2x mb-3" />
                            <p>Select a trend from the left to begin.</p>
                        </div>
                    {:else}
                        <div class="alert alert-info mb-4">
                            <strong>Selected Trend:</strong>
                            {selectedTrend.trend_name}
                        </div>

                        <form on:submit|preventDefault={generatePlan}>
                            <div class="mb-3">
                                <label for="product" class="form-label"
                                    >Product/Service to Market <span class="text-danger">*</span></label
                                >
                                <input
                                    type="text"
                                    class="form-control"
                                    id="product"
                                    bind:value={product}
                                    placeholder="e.g., Our new 'Pandan Gula Melaka' Latte"
                                    required
                                />
                            </div>

                            <div class="mb-3">
                                <label for="objective" class="form-label"
                                    >Marketing Objective <span class="text-danger">*</span></label
                                >
                                <input
                                    type="text"
                                    class="form-control"
                                    id="objective"
                                    bind:value={objective}
                                    placeholder="e.g., Drive trial and awareness"
                                    required
                                />
                            </div>

                            <div class="mb-3">
                                <label for="cta" class="form-label">Call to Action</label>
                                <input
                                    type="text"
                                    class="form-control"
                                    id="cta"
                                    bind:value={call_to_action}
                                    placeholder="e.g., Come in and try one today!"
                                />
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label for="medium" class="form-label">Content Medium</label>
                                    <select class="form-select" id="medium" bind:value={content_medium}>
                                        {#each contentMediums as medium}
                                            <option value={medium}>{medium}</option>
                                        {/each}
                                    </select>
                                </div>

                                <div class="col-md-6 mb-3">
                                    <label for="tone" class="form-label">Tone</label>
                                    <select class="form-select" id="tone" bind:value={tone}>
                                        {#each tones as toneOption}
                                            <option value={toneOption}>{toneOption}</option>
                                        {/each}
                                    </select>
                                </div>
                            </div>

                            <button
                                type="submit"
                                class="btn btn-primary btn-lg w-100"
                                disabled={isGenerating || !product || !objective}
                            >
                                {#if isGenerating}
                                    <span class="spinner-border spinner-border-sm me-2" role="status" />
                                    Generating Plan...
                                {:else}
                                    <i class="fas fa-magic me-2" />
                                    Generate Content Plan
                                {/if}
                            </button>
                        </form>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .idea-generator-container {
        margin-bottom: 2rem;
    }
    .trends-list {
        max-height: 600px;
        overflow-y: auto;
        padding-right: 10px;
    }
    .trend-item {
        cursor: pointer;
        transition:
            background-color 0.2s ease-in-out,
            border-color 0.2s ease-in-out;
    }
    .trend-item:hover {
        background-color: #f8f9fa;
    }
    .trend-item.active {
        border-color: #667eea !important;
        background-color: #f0f2ff;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    .trend-item img {
        max-height: 150px;
        width: 100%;
        object-fit: cover;
    }
</style>
