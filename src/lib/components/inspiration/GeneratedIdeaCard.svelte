<script>
    export let idea;
</script>

<div class="idea-card">
    <div class="card-header">
        <div class="idea-icon">
            <i class="fas fa-lightbulb"></i>
        </div>
        <h5 class="card-title">{idea.title}</h5>
    </div>
    
    <div class="card-body">
        <p class="card-description">{idea.description}</p>
        
        {#if idea.tags}
            <div class="tags-section">
                {#each idea.tags as tag}
                    <span class="tag-badge">{tag}</span>
                {/each}
            </div>
        {/if}
        
        {#if idea.intent}
            <div class="intent-section">
                <div class="intent-label">
                    <i class="fas fa-bullseye"></i>
                    <span>Intent: {idea.intent}</span>
                </div>
            </div>
        {/if}
    </div>
    
    <div class="card-actions">
        <button class="action-btn use-btn">
            <i class="fas fa-plus"></i>
            Use Idea
        </button>
        <button class="action-btn save-btn">
            <i class="fas fa-bookmark"></i>
            Save
        </button>
        <button class="action-btn share-btn">
            <i class="fas fa-share"></i>
            Share
        </button>
    </div>
</div>

<style>
    .idea-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        overflow: hidden;
        height: 100%;
        margin-bottom: 1rem;
        position: relative;
    }

    .idea-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .idea-card:hover::before {
        opacity: 1;
    }

    .idea-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .card-header {
        padding: 1.5rem 1.5rem 1rem;
        position: relative;
        z-index: 2;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }

    .idea-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.1rem;
        flex-shrink: 0;
    }

    .card-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.1rem;
        line-height: 1.3;
        flex: 1;
    }

    .card-body {
        padding: 0 1.5rem 1rem;
        position: relative;
        z-index: 2;
    }

    .card-description {
        color: #4a5568;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .tags-section {
        margin-bottom: 1rem;
    }

    .tag-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        margin-right: 0.5rem;
        margin-bottom: 0.25rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .intent-section {
        margin-bottom: 0.5rem;
    }

    .intent-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #718096;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .intent-label i {
        color: #667eea;
        font-size: 0.8rem;
    }

    .card-actions {
        padding: 1rem 1.5rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        gap: 0.5rem;
        position: relative;
        z-index: 2;
        background: rgba(255, 255, 255, 0.5);
    }

    .action-btn {
        flex: 1;
        border: none;
        padding: 0.6rem 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
    }

    .use-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .use-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    .save-btn {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .save-btn:hover {
        background: rgba(16, 185, 129, 0.2);
        transform: translateY(-1px);
    }

    .share-btn {
        background: rgba(245, 158, 11, 0.1);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }

    .share-btn:hover {
        background: rgba(245, 158, 11, 0.2);
        transform: translateY(-1px);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .card-header {
            padding: 1rem 1rem 0.75rem;
            flex-direction: column;
            text-align: center;
            gap: 0.75rem;
        }

        .card-body {
            padding: 0 1rem 0.75rem;
        }

        .card-actions {
            padding: 0.75rem 1rem;
            flex-direction: column;
            gap: 0.5rem;
        }

        .action-btn {
            padding: 0.7rem 1rem;
            font-size: 0.85rem;
        }
    }
</style>