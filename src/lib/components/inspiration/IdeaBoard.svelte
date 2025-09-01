<script>
    import GeneratedIdeaCard from "./GeneratedIdeaCard.svelte";
    import { goto } from "$app/navigation";
    import { showToast } from "$lib/stores/toastStore.js";

    /** @type {any | null} */
    export let generatedPlan = null;
    export let isLoading = false;

    let isSubmitting = false;
    let isSubmitted = false;

    async function addPlanToBoard() {
        if (!generatedPlan || !generatedPlan.plan || isSubmitted) return;

        isSubmitting = true;

        try {
            const formattedContent = generatedPlan.plan
                .map(
                    /** @param {{ day: string, task: string, details: string }} step */
                    (step) => `### ${step.day}: ${step.task}\n${step.details}`
                )
                .join("\n\n---\n\n");

            const response = await fetch("/api/collaborate/cards", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    title: generatedPlan.plan_title,
                    description: `AI-generated ${generatedPlan.content_medium} content plan`,
                    content: formattedContent,
                    status: "Ideas",
                    platform: generatedPlan.content_medium || "Multiple Platforms",
                    assignee: "Content Team",
                    image: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop&crop=center",
                    notes: "Generated from AI content planning tool"
                }),
            });

            if (response.ok) {
                isSubmitted = true;
                showToast("Plan added successfully!", "View on Board", () =>
                    goto("/collaborate"),
                );
            } else {
                throw new Error("Failed to add plan to board");
            }
        } catch (error) {
            console.error("Error adding plan to board:", error);
            showToast("Error: Could not add plan.", "Retry", addPlanToBoard);
        } finally {
            isSubmitting = false;
        }
    }
</script>

<div class="idea-board">
    <div class="board-header">
        <div class="step-number">3</div>
        <div class="header-info">
            <h2 class="board-title">Your Generated Content Plan</h2>
            <p class="board-subtitle">
                Review the AI-generated plan and add it to your content board for collaboration.
            </p>
        </div>
    </div>

    <div class="board-content">
        {#if isLoading}
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <h4 class="loading-title">Generating your plan...</h4>
                <p class="loading-text">
                    The AI is crafting a personalized content strategy for you. This may take a moment.
                </p>
            </div>
        {:else if generatedPlan && generatedPlan.plan}
            <div class="plan-preview">
                <div class="plan-header">
                    <h3 class="plan-title">{generatedPlan.plan_title}</h3>
                    <div class="plan-meta">
                        <span class="plan-badge">{generatedPlan.content_medium}</span>
                        <span class="plan-count">{generatedPlan.plan.length} steps</span>
                    </div>
                </div>

                <div class="action-section">
                    <button
                        class="add-to-board-btn"
                        on:click={addPlanToBoard}
                        disabled={isSubmitting || isSubmitted}
                    >
                        {#if isSubmitting}
                            <div class="btn-spinner"></div>
                            Adding to Board...
                        {:else if isSubmitted}
                            <i class="fas fa-check"></i>
                            Added to Board!
                        {:else}
                            <i class="fas fa-plus"></i>
                            Add Entire Plan to Board
                        {/if}
                    </button>
                </div>

                <div class="ideas-container">
                    {#each generatedPlan.plan as idea, i (i)}
                        <GeneratedIdeaCard {idea} />
                    {/each}
                </div>
            </div>
        {:else}
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-wand-magic-sparkles"></i>
                </div>
                <h4 class="empty-title">Your plan will appear here</h4>
                <p class="empty-description">
                    Select a trending topic and fill out the form above to generate your
                    personalized content plan.
                </p>
            </div>
        {/if}
    </div>
</div>

<style>
    .idea-board {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        max-width: 1400px; /* Match the generator container width */
        width: 100%;
        margin: 0 auto; /* Center the container */
    }

    .board-header {
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

    .header-info {
        flex: 1;
    }

    .board-title {
        margin: 0 0 0.5rem 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        line-height: 1.3;
    }

    .board-subtitle {
        margin: 0;
        color: #718096;
        font-size: 1rem;
        font-weight: 500;
    }

    .board-content {
        padding: 2rem;
        flex: 1; /* Allows content to expand and fill available space */
        display: flex;
        flex-direction: column;
    }

    /* Loading State */
    .loading-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #718096;
    }

    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 4px solid rgba(102, 126, 234, 0.1);
        border-top: 4px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 2rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .loading-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
        margin: 0 0 1rem 0;
    }

    .loading-text {
        color: #718096;
        font-size: 1rem;
        margin: 0;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }

    /* Plan Preview */
    .plan-preview {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    .plan-header {
        text-align: center;
        padding: 2rem;
        background: rgba(102, 126, 234, 0.02);
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .plan-title {
        font-weight: 700;
        color: #2d3748;
        margin: 0 0 1rem 0;
        font-size: 1.5rem;
        line-height: 1.3;
    }

    .plan-meta {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .plan-badge {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        color: #667eea;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .plan-count {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Action Section */
    .action-section {
        text-align: center;
    }

    .add-to-board-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        min-width: 250px;
        justify-content: center;
    }

    .add-to-board-btn:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .add-to-board-btn:disabled {
        opacity: 0.7;
        cursor: not-allowed;
        transform: none;
    }

    .btn-spinner {
        width: 18px;
        height: 18px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top: 2px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    /* Ideas Container */
    .ideas-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #718096;
        background: rgba(102, 126, 234, 0.02);
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .empty-icon {
        font-size: 3rem;
        color: #667eea;
        margin-bottom: 1.5rem;
        opacity: 0.7;
    }

    .empty-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
        margin: 0 0 1rem 0;
    }

    .empty-description {
        color: #718096;
        font-size: 1rem;
        margin: 0;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.5;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .board-header {
            padding: 1.5rem 1.5rem 1rem;
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }

        .board-content {
            padding: 1.5rem;
        }

        .plan-header {
            padding: 1.5rem;
        }

        .plan-title {
            font-size: 1.3rem;
        }

        .step-number {
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
        }

        .board-title {
            font-size: 1.3rem;
        }

        .ideas-container {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .add-to-board-btn {
            width: 100%;
            min-width: auto;
        }

        .loading-state, .empty-state {
            padding: 3rem 1.5rem;
        }

        .plan-meta {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
</style>
