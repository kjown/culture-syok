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

<div class="generator-container">
    <!-- Step 1: Trend Selection -->
    <div class="step-card">
        <div class="step-header">
            <div class="step-number">1</div>
            <div class="step-info">
                <h2 class="step-title">Select a Trending Topic</h2>
                <p class="step-subtitle">Choose from current trending topics to inspire your content</p>
            </div>
        </div>
        
        <div class="step-content">
            {#if loadingTrends}
                <div class="loading-state">
                    <div class="spinner"></div>
                    <p>Loading trending topics...</p>
                </div>
            {:else if availableTrends.length > 0}
                <div class="trends-grid">
                    {#each availableTrends as trend (trend.trend_name)}
                        <div
                            class="trend-card"
                            class:selected={selectedTrend?.trend_name === trend.trend_name}
                            on:click={() => handleSelectTrend(trend)}
                            on:keydown={(e) => e.key === 'Enter' && handleSelectTrend(trend)}
                            role="button"
                            tabindex="0"
                        >
                            {#if trend.representative_image_url}
                                <div class="trend-image">
                                    <img
                                        src={trend.representative_image_url}
                                        alt={trend.trend_name}
                                        loading="lazy"
                                    />
                                </div>
                            {/if}
                            <div class="trend-content">
                                <h3 class="trend-title">{trend.trend_name}</h3>
                                <p class="trend-description">{trend.description}</p>
                            </div>
                            <div class="trend-overlay">
                                <i class="fas fa-check"></i>
                            </div>
                        </div>
                    {/each}
                </div>
            {:else}
                <div class="empty-state">
                    <i class="fas fa-chart-line"></i>
                    <p>No trending topics available at the moment.</p>
                </div>
            {/if}
        </div>
    </div>

    <!-- Step 2: Content Plan Generation -->
    <div class="step-card" class:disabled={!selectedTrend}>
        <div class="step-header">
            <div class="step-number">2</div>
            <div class="step-info">
                <h2 class="step-title">Generate Content Plan</h2>
                <p class="step-subtitle">Tell us about your product and goals to create a personalized plan</p>
            </div>
        </div>
        
        <div class="step-content">
            {#if !selectedTrend}
                <div class="placeholder-state">
                    <i class="fas fa-arrow-up"></i>
                    <p>Please select a trending topic above to continue</p>
                </div>
            {:else}
                <div class="selected-trend-info">
                    <div class="trend-badge">
                        <i class="fas fa-fire"></i>
                        <span>Selected: {selectedTrend.trend_name}</span>
                    </div>
                </div>

                <form on:submit|preventDefault={generatePlan} class="content-form">
                    <div class="form-row">
                        <div class="input-group">
                            <label for="product" class="input-label">
                                Product/Service <span class="required">*</span>
                            </label>
                            <input
                                type="text"
                                id="product"
                                class="form-input"
                                bind:value={product}
                                placeholder="e.g., Our new 'Pandan Gula Melaka' Latte"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="input-group">
                            <label for="objective" class="input-label">
                                Marketing Objective <span class="required">*</span>
                            </label>
                            <input
                                type="text"
                                id="objective"
                                class="form-input"
                                bind:value={objective}
                                placeholder="e.g., Drive trial and awareness"
                                required
                            />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="input-group">
                            <label for="cta" class="input-label">
                                Call to Action <span class="optional">(Optional)</span>
                            </label>
                            <input
                                type="text"
                                id="cta"
                                class="form-input"
                                bind:value={call_to_action}
                                placeholder="e.g., Come in and try one today!"
                            />
                        </div>
                    </div>

                    <div class="form-row form-row-split">
                        <div class="input-group">
                            <label for="medium" class="input-label">Content Medium</label>
                            <select class="form-select" id="medium" bind:value={content_medium}>
                                {#each contentMediums as medium}
                                    <option value={medium}>{medium}</option>
                                {/each}
                            </select>
                        </div>

                        <div class="input-group">
                            <label for="tone" class="input-label">Tone</label>
                            <select class="form-select" id="tone" bind:value={tone}>
                                {#each tones as toneOption}
                                    <option value={toneOption}>{toneOption}</option>
                                {/each}
                            </select>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button
                            type="submit"
                            class="generate-btn"
                            disabled={isGenerating || !product || !objective}
                        >
                            {#if isGenerating}
                                <div class="btn-spinner"></div>
                                Generating Plan...
                            {:else}
                                <i class="fas fa-magic"></i>
                                Generate Content Plan
                            {/if}
                        </button>
                    </div>
                </form>
            {/if}
        </div>
    </div>
</div>

<style>
    .generator-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        max-width: 1400px; /* Match the parent container width */
        width: 100%;
        margin: 0 auto;
    }

    .step-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        transition: all 0.3s ease;
        min-height: 650px; /* Increased for better consistency */
        display: flex;
        flex-direction: column;
    }

    .step-card.disabled {
        opacity: 0.6;
        pointer-events: none;
    }

    .step-header {
        padding: 2rem 2rem 1rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        border-bottom: 1px solid rgba(102, 126, 234, 0.1);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.03) 0%, rgba(118, 75, 162, 0.03) 100%);
    }

    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        flex-shrink: 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .step-info {
        flex: 1;
    }

    .step-title {
        margin: 0 0 0.5rem 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        line-height: 1.3;
    }

    .step-subtitle {
        margin: 0;
        color: #718096;
        font-size: 1rem;
        font-weight: 500;
    }

    .step-content {
        padding: 2rem;
        flex: 1; /* Allows content to expand and fill available space */
        display: flex;
        flex-direction: column;
    }

    /* Loading State */
    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        color: #718096;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid rgba(102, 126, 234, 0.1);
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Trends Grid */
    .trends-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .trend-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.1);
        overflow: hidden;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        min-height: 200px;
    }

    .trend-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .trend-card.selected {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }

    .trend-card.selected .trend-overlay {
        opacity: 1;
    }

    .trend-image {
        width: 100%;
        height: 150px;
        overflow: hidden;
        position: relative;
    }

    .trend-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .trend-card:hover .trend-image img {
        transform: scale(1.05);
    }

    .trend-content {
        padding: 1.5rem;
    }

    .trend-title {
        margin: 0 0 0.75rem 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.1rem;
        line-height: 1.3;
    }

    .trend-description {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .trend-overlay {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 35px;
        height: 35px;
        background: #667eea;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        opacity: 0;
        transition: opacity 0.3s ease;
        font-size: 0.9rem;
    }

    /* Placeholder States */
    .placeholder-state, .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        color: #9ca3af;
        text-align: center;
    }

    .placeholder-state i, .empty-state i {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }

    /* Selected Trend Info */
    .selected-trend-info {
        margin-bottom: 2rem;
    }

    .trend-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.25rem;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    /* Form Styles */
    .content-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .form-row {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .form-row-split {
        flex-direction: row;
        gap: 1.5rem;
    }

    .input-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        flex: 1;
    }

    .input-label {
        font-weight: 600;
        color: #2d3748;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .required {
        color: #e53e3e;
        font-size: 0.8rem;
    }

    .optional {
        color: #9ca3af;
        font-size: 0.8rem;
        font-weight: 400;
    }

    .form-input, .form-select {
        padding: 1rem 1.25rem;
        border: 2px solid rgba(102, 126, 234, 0.1);
        border-radius: 12px !important; /* Force border-radius on all sides */
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        color: #2d3748;
        box-sizing: border-box; /* Ensure proper box model */
        -webkit-border-radius: 12px !important; /* WebKit browsers */
        -moz-border-radius: 12px !important; /* Firefox */
    }

    /* Ensure Bootstrap doesn't override our styling */
    .step-content .form-input,
    .step-content .form-select {
        border-radius: 12px !important;
        -webkit-border-radius: 12px !important;
        -moz-border-radius: 12px !important;
    }

    .form-input:focus, .form-select:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: rgba(255, 255, 255, 0.95);
    }

    .form-input::placeholder {
        color: #9ca3af;
    }

    .form-select {
        cursor: pointer;
        appearance: none;
        width: 100%;
        min-width: 0; /* Allows flex items to shrink properly */
        background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%23667eea' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
        background-position: right 1rem center;
        background-repeat: no-repeat;
        background-size: 1rem;
        padding-right: 3rem;
    }

    .form-select:focus {
        background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%23667eea' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
    }

    /* Generate Button */
    .form-actions {
        margin-top: 1rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(102, 126, 234, 0.1);
    }

    .generate-btn {
        width: 100%;
        padding: 1.25rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .generate-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .generate-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }

    .btn-spinner {
        width: 20px;
        height: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .generator-container {
            gap: 1.5rem;
        }

        .step-header {
            padding: 1.5rem 1.5rem 1rem;
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }

        .step-content {
            padding: 1.5rem;
        }

        .trends-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .form-row-split {
            flex-direction: column;
            gap: 1rem;
        }

        .step-title {
            font-size: 1.3rem;
        }

        .step-number {
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
        }
    }
</style>