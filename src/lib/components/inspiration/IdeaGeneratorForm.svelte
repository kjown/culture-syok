<script>
    import { createEventDispatcher, onMount } from 'svelte';

    const dispatch = createEventDispatcher();

    /**
     * @typedef {Object} GeneratedIdea
     * @property {string} title
     * @property {string} description
     * @property {string[]} [tags]
     * @property {string} [intent]
     */

    /** @type {any[]} */
    let availableTrends = [];
    /** @type {any | null} */
    let selectedTrend = null;
    let loadingTrends = true;
    let isGenerating = false;

    // form fields
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
        const cachedTrends = sessionStorage.getItem('trendsData');
        
        if (cachedTrends) {
            availableTrends = JSON.parse(cachedTrends);
            loadingTrends = false;
            return; 
        }
        try {
            // NOTE: Ensure your FastAPI server is running on port 8000
            const response = await fetch('http://127.0.0.1:8000/api/get-trends');
            if (response.ok) {
                const data = await response.json();
                availableTrends = data.trends || [];
                sessionStorage.setItem('trendsData', JSON.stringify(availableTrends));
            } else {
                console.error('Failed to fetch trends:', response.status);
            }
        } catch (error) {
            console.error('Error fetching trends:', error);
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
        } finally {
            isGenerating = false;
        }
    }
</script>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Trends Selection Column -->
    <div class="lg:col-span-1">
        <div class="styled-card">
            <div class="styled-card-header">
                <div class="header-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div>
                    <h2 class="header-title">1. Select a Trend</h2>
                    <p class="header-subtitle">Browse topics to find inspiration.</p>
                </div>
            </div>
            <div class="styled-card-body">
                {#if loadingTrends}
                    <div class="flex justify-center items-center h-full">
                        <span class="loading loading-spinner loading-lg text-primary"></span>
                    </div>
                {:else if availableTrends.length > 0}
                    <div class="trends-list space-y-4">
                        {#each availableTrends as trend (trend.trend_name)}
                            <div
                                class="trend-item"
                                class:selected={selectedTrend?.trend_name === trend.trend_name}
                                on:click={() => handleSelectTrend(trend)}
                                on:keydown={(e) => e.key === 'Enter' && handleSelectTrend(trend)}
                                role="button"
                                tabindex="0"
                            >
                                <h3 class="font-semibold text-sm mb-2 text-gray-800">{trend.trend_name}</h3>
                                <p class="text-xs text-gray-600 mb-2 line-clamp-3">{trend.description}</p>
                                {#if trend.representative_image_url}
                                    <img
                                        src={trend.representative_image_url}
                                        alt={trend.trend_name}
                                        class="w-full h-32 object-cover rounded-md"
                                    />
                                {/if}
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p class="text-gray-500">No trends available.</p>
                {/if}
            </div>
        </div>
    </div>

    <!-- Content Plan Form Column -->
    <div class="lg:col-span-2">
        <div class="styled-card">
            <div class="styled-card-header">
                 <div class="header-icon">
                    <i class="fas fa-pen-alt"></i>
                </div>
                <div>
                    <h2 class="header-title">2. Generate Content Plan</h2>
                    <p class="header-subtitle">Create a plan based on your selected trend.</p>
                </div>
            </div>
            <div class="styled-card-body">
                {#if !selectedTrend}
                    <div class="flex flex-col items-center justify-center h-full text-center">
                        <i class="fas fa-arrow-left text-3xl mb-4 text-gray-300"></i>
                        <p class="text-gray-500">Select a trend from the left to begin.</p>
                    </div>
                {:else}
                    <div class="alert alert-info mb-6">
                        <i class="fas fa-info-circle"></i>
                        <div>
                            <h3 class="font-bold">Selected Trend</h3>
                            <div class="text-sm">{selectedTrend.trend_name}</div>
                        </div>
                    </div>

                    <form on:submit|preventDefault={generatePlan} class="space-y-4">
                        <div class="form-control">
                            <label for="product" class="label">
                                <span class="label-text">Product/Service to Market <span class="text-error">*</span></span>
                            </label>
                            <input
                                type="text"
                                id="product"
                                class="input input-bordered w-full"
                                bind:value={product}
                                placeholder="e.g., Our new 'Pandan Gula Melaka' Latte"
                                required
                            />
                        </div>

                        <div class="form-control">
                            <label for="objective" class="label">
                                <span class="label-text">Marketing Objective <span class="text-error">*</span></span>
                            </label>
                            <input
                                type="text"
                                id="objective"
                                class="input input-bordered w-full"
                                bind:value={objective}
                                placeholder="e.g., Drive trial and awareness"
                                required
                            />
                        </div>

                        <div class="form-control">
                            <label for="cta" class="label">
                                <span class="label-text">Call to Action</span>
                            </label>
                            <input
                                type="text"
                                id="cta"
                                class="input input-bordered w-full"
                                bind:value={call_to_action}
                                placeholder="e.g., Come in and try one today!"
                            />
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div class="form-control">
                                <label for="medium" class="label">
                                    <span class="label-text">Content Medium</span>
                                </label>
                                <select class="select select-bordered" id="medium" bind:value={content_medium}>
                                    {#each contentMediums as medium}
                                        <option value={medium}>{medium}</option>
                                    {/each}
                                </select>
                            </div>

                            <div class="form-control">
                                <label for="tone" class="label">
                                    <span class="label-text">Tone</span>
                                </label>
                                <select class="select select-bordered" id="tone" bind:value={tone}>
                                    {#each tones as toneOption}
                                        <option value={toneOption}>{toneOption}</option>
                                    {/each}
                                </select>
                            </div>
                        </div>

                        <div class="pt-4">
                            <button
                                type="submit"
                                class="btn btn-primary btn-lg w-full"
                                disabled={isGenerating || !product || !objective}
                            >
                                {#if isGenerating}
                                    <span class="loading loading-spinner"></span>
                                    Generating Plan...
                                {:else}
                                    <i class="fas fa-magic me-2"></i>
                                    Generate Content Plan
                                {/if}
                            </button>
                        </div>
                    </form>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .styled-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .styled-card-header {
        padding: 1.5rem 1.5rem 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        border-bottom: 1px solid #f1f5f9;
    }

    .header-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #667eea;
        font-size: 1.1rem;
        flex-shrink: 0;
    }

    .header-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.25rem; /* Matched to IdeaBoard title size */
        line-height: 1.3;
    }

    .header-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.95rem; /* Matched to IdeaBoard subtitle size */
        font-weight: 400;
    }

    .styled-card-body {
        padding: 1rem 1.5rem 1.5rem;
        flex-grow: 1;
        overflow-y: auto;
    }

    .trends-list {
        max-height: 65vh;
        overflow-y: auto;
        padding-right: 0.5rem;
        margin-right: -0.5rem;
    }
    .trend-item {
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        background-color: #f8fafc;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    .trend-item:hover {
        border-color: #cbd5e1;
        background-color: #f1f5f9;
    }
    .trend-item.selected {
        border-color: #667eea;
        background-color: rgba(102, 126, 234, 0.1);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    .line-clamp-3 {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>
