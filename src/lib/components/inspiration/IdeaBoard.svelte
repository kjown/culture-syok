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
                    content: formattedContent,
                    status: "Ideas",
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
        <div class="header-icon">
            <i class="fas fa-clipboard-list" />
        </div>
        <div>
            <h2 class="board-title">3. Your Generated Content Plan</h2>
            <p class="board-subtitle">
                Review the AI-generated plan and add it to your content board.
            </p>
        </div>
    </div>

    <div class="board-content">
        {#if isLoading}
            <div class="text-center p-5">
                <div
                    class="spinner-border text-primary"
                    style="width: 3rem; height: 3rem;"
                    role="status"
                >
                    <span class="visually-hidden">Loading...</span>
                </div>
                <h4 class="mt-3">Generating your plan...</h4>
                <p class="text-muted">
                    The AI is working its magic. This may take a moment.
                </p>
            </div>
        {:else if generatedPlan && generatedPlan.plan}
            <div class="plan-header mb-4">
                <h3 class="plan-title">{generatedPlan.plan_title}</h3>
                <span class="badge bg-primary-soft text-primary"
                    >{generatedPlan.content_medium}</span
                >
            </div>

            <div class="text-center mb-4">
                <button
                    class="btn btn-primary btn-lg"
                    on:click={addPlanToBoard}
                    disabled={isSubmitting || isSubmitted}
                >
                    {#if isSubmitting}
                        <span
                            class="spinner-border spinner-border-sm me-2"
                            role="status"
                        />
                        Adding to Board...
                    {:else if isSubmitted}
                        <i class="fas fa-check me-2" />
                        Added to Board!
                    {:else}
                        <i class="fas fa-plus me-2" />
                        Add Entire Plan to Board
                    {/if}
                </button>
            </div>

            <div class="ideas-container">
                {#each generatedPlan.plan as idea, i (i)}
                    <GeneratedIdeaCard {idea} />
                {/each}
            </div>
        {:else}
            <div class="empty-state p-5">
                <div class="empty-icon">
                    <i class="fas fa-wand-magic-sparkles" />
                </div>
                <h4 class="empty-title">Your plan will appear here</h4>
                <p class="empty-description">
                    Select a trend and fill out the form above to generate your
                    custom content plan.
                </p>
            </div>
        {/if}
    </div>
</div>

<style>
    .idea-board {
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.05);
    }
    .board-header {
        padding: 2rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .header-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(
            135deg,
            rgba(102, 126, 234, 0.1) 0%,
            rgba(118, 75, 162, 0.1) 100%
        );
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #667eea;
        font-size: 1.5rem;
        flex-shrink: 0;
    }
    .board-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
    }
    .board-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.95rem;
    }
    .board-content {
        padding: 0 2rem 2rem;
    }
    .ideas-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    .plan-header {
        text-align: center;
        padding-bottom: 1.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 1px solid #f1f5f9;
    }
    .plan-title {
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    .badge.bg-primary-soft {
        background-color: rgba(102, 126, 234, 0.1);
        color: #667eea;
        font-weight: 600;
        padding: 0.5em 1em;
    }
    .empty-state {
        text-align: center;
        color: #718096;
        background-color: #f7fafc;
        border-radius: 12px;
    }
    .empty-icon {
        font-size: 2.5rem;
        color: #667eea;
        margin-bottom: 1rem;
    }
</style>
