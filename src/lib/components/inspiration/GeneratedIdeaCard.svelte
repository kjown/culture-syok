<script>
    /** @type {{day: string, task: string, details: string}} */
    export let idea;
</script>

<div class="idea-card">
    <div class="card-header">
        <div class="idea-icon">
            <i class="fas fa-calendar-day" />
        </div>
        <div>
            <h5 class="card-title">{idea.day}: {idea.task}</h5>
        </div>
    </div>

    <div class="card-body">
        <p class="card-description">{idea.details}</p>
    </div>
</div>

<style>
    .idea-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .card-header {
        padding: 1.5rem 1.5rem 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        border-bottom: 1px solid #f1f5f9;
    }

    .idea-icon {
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

    .card-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.1rem;
        line-height: 1.3;
    }

    .card-body {
        padding: 1rem 1.5rem 1.5rem;
        flex-grow: 1;
    }

    .card-description {
        color: #4a5568;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }
</style>