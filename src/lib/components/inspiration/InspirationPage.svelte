<script>
    import IdeaGeneratorForm from './IdeaGeneratorForm.svelte';
    import IdeaBoard from './IdeaBoard.svelte';

    /** @type {any | null} */
    let generatedPlan = null;
    let isLoading = false;

    /**
     * @param {CustomEvent<any>} event
     */
    function handlePlanGenerated(event) {
        generatedPlan = event.detail;
        isLoading = false;
    }
</script>

<div class="inspiration-container">
    <div class="page-header">
        <h1 class="page-title">
            <i class="fas fa-lightbulb me-3"></i>
            Content Inspiration
        </h1>
        <p class="page-subtitle">Discover trending topics and generate creative content ideas powered by AI</p>
    </div>

    <div class="content-wrapper">
        <!-- Main content generation form -->
        <IdeaGeneratorForm on:loading={() => (isLoading = true)} on:planGenerated={handlePlanGenerated} />
        
        <!-- Generated plan display -->
        <IdeaBoard {generatedPlan} {isLoading} />
    </div>
</div>

<style>
    .inspiration-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem 1rem;
        min-height: 100vh;
    }

    .page-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
        position: relative;
    }

    .page-title {
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .page-title i {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .page-subtitle {
        color: #718096;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .content-wrapper {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .inspiration-container {
            padding: 1.5rem 1rem;
        }

        .page-title {
            font-size: 2rem;
            flex-direction: column;
            gap: 0.5rem;
        }

        .page-subtitle {
            font-size: 1rem;
        }

        .page-header {
            margin-bottom: 2rem;
            padding: 1.5rem 0;
        }
    }
</style>
