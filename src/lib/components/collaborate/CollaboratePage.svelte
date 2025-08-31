<script>
    let ideas = [
        { image: "/images/idea1.png" },
        { image: "/images/idea2.png" },
        { image: "/images/idea3.png" },
    ];
    let activeTab = "Ideas";
    let tabs = ["Ideas", "To Do", "In Review", "Approved"];
    let link = "";
    let date = "";
    let time = "";
    let reminder = "";
</script>

<div class="collaborate-container">
    <!-- Enhanced Page Header -->
    <div class="page-header">
        <h1 class="page-title">
            <i class="fas fa-users me-3"></i>
            Team Collaboration
        </h1>
        <p class="page-subtitle">Collaborate with your team to plan, review, and approve content across all platforms</p>
    </div>

    <div class="collaboration-workspace">
        <!-- Main Content: Content Plan Board -->
        <div class="content-board">
            <div class="board-header">
                <div class="header-icon">
                    <i class="fas fa-project-diagram"></i>
                </div>
                <div>
                    <h3 class="board-title">Content Pipeline</h3>
                    <p class="board-subtitle">Track your content through every stage of production</p>
                </div>
            </div>

            <!-- Enhanced Tab Navigation -->
            <div class="tab-navigation">
                {#each tabs as tab}
                    <button
                        class="tab-btn"
                        class:active={activeTab === tab}
                        type="button"
                        on:click={() => (activeTab = tab)}
                    >
                        <div class="tab-content">
                            <span class="tab-label">{tab}</span>
                            <span class="tab-count">({ideas.length})</span>
                        </div>
                        {#if tab === "Ideas"}
                            <i class="fas fa-lightbulb tab-icon"></i>
                        {:else if tab === "To Do"}
                            <i class="fas fa-list-check tab-icon"></i>
                        {:else if tab === "In Review"}
                            <i class="fas fa-eye tab-icon"></i>
                        {:else if tab === "Approved"}
                            <i class="fas fa-check-circle tab-icon"></i>
                        {/if}
                    </button>
                {/each}
            </div>

            <!-- Tab Content -->
            <div class="tab-content-area">
                {#if ideas.length > 0}
                    <div class="ideas-grid">
                        {#each ideas as idea, index}
                            <div class="idea-card">
                                <div class="card-image">
                                    <img
                                        src={idea.image}
                                        alt="Content Idea {index + 1}"
                                        class="idea-image"
                                    />
                                    <div class="image-overlay">
                                        <button class="overlay-btn view-btn">
                                            <i class="fas fa-eye"></i>
                                        </button>
                                        <button class="overlay-btn edit-btn">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="overlay-btn move-btn">
                                            <i class="fas fa-arrow-right"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="card-content">
                                    <h6 class="idea-title">Content Idea #{index + 1}</h6>
                                    <p class="idea-description">Creative concept for social media campaign</p>
                                    <div class="idea-meta">
                                        <span class="status-badge {activeTab.toLowerCase().replace(' ', '-')}">
                                            {activeTab}
                                        </span>
                                        <span class="date-badge">
                                            <i class="fas fa-clock"></i>
                                            2 days ago
                                        </span>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                {:else}
                    <div class="empty-state">
                        <div class="empty-icon">
                            {#if activeTab === "Ideas"}
                                <i class="fas fa-lightbulb"></i>
                            {:else if activeTab === "To Do"}
                                <i class="fas fa-tasks"></i>
                            {:else if activeTab === "In Review"}
                                <i class="fas fa-search"></i>
                            {:else}
                                <i class="fas fa-check-circle"></i>
                            {/if}
                        </div>
                        <h4 class="empty-title">No content in {activeTab.toLowerCase()}</h4>
                        <p class="empty-description">
                            {#if activeTab === "Ideas"}
                                Start by adding new content ideas to your pipeline.
                            {:else if activeTab === "To Do"}
                                Move ideas here when they're ready to be developed.
                            {:else if activeTab === "In Review"}
                                Content awaiting review will appear here.
                            {:else}
                                Approved content ready for publishing will be shown here.
                            {/if}
                        </p>
                        <button class="empty-action-btn">
                            <i class="fas fa-plus"></i>
                            Add New Content
                        </button>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    .collaborate-container {
        padding: 2rem 0;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* Page Header */
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

    /* Collaboration Workspace */
    .collaboration-workspace {
        display: grid;
        gap: 2rem;
    }

    .content-board {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .board-header {
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

    .board-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .board-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Tab Navigation */
    .tab-navigation {
        display: flex;
        gap: 0.5rem;
        margin: 2rem;
        margin-bottom: 0;
        background: rgba(102, 126, 234, 0.03);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .tab-btn {
        flex: 1;
        background: transparent;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .tab-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .tab-btn:hover::before {
        opacity: 1;
    }

    .tab-btn.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transform: translateY(-1px);
    }

    .tab-btn.active .tab-content {
        color: white;
    }

    .tab-btn.active .tab-icon {
        color: white;
    }

    .tab-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        z-index: 2;
        color: #4a5568;
        font-weight: 600;
    }

    .tab-label {
        font-size: 0.95rem;
    }

    .tab-count {
        font-size: 0.8rem;
        opacity: 0.8;
    }

    .tab-icon {
        color: #667eea;
        font-size: 1.1rem;
        transition: color 0.3s ease;
    }

    /* Content Area */
    .tab-content-area {
        padding: 2rem;
        min-height: 400px;
    }

    .ideas-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }

    .idea-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
    }

    .idea-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .card-image {
        position: relative;
        height: 200px;
        overflow: hidden;
    }

    .idea-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .idea-card:hover .idea-image {
        transform: scale(1.05);
    }

    .image-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .idea-card:hover .image-overlay {
        opacity: 1;
    }

    .overlay-btn {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        color: #667eea;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
    }

    .overlay-btn:hover {
        background: white;
        transform: scale(1.1);
    }

    .card-content {
        padding: 1.5rem;
    }

    .idea-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .idea-description {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .idea-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .status-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
    }

    .status-badge.ideas {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }

    .status-badge.to-do {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }

    .status-badge.in-review {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }

    .status-badge.approved {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    .date-badge {
        color: #9ca3af;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #718096;
    }

    .empty-icon {
        width: 80px;
        height: 80px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 2rem;
        color: #667eea;
    }

    .empty-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 0.75rem;
    }

    .empty-description {
        color: #718096;
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 2rem;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }

    .empty-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 0.875rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .empty-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* Responsive design */
    @media (max-width: 1200px) {
        .collaborate-container {
            padding: 1.5rem 1rem;
        }
    }

    @media (max-width: 768px) {
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

        .board-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            text-align: center;
        }

        .tab-navigation {
            margin: 1.5rem 1rem 0;
            flex-direction: column;
            gap: 0.5rem;
        }

        .tab-btn {
            padding: 0.875rem 1rem;
        }

        .tab-content-area {
            padding: 1.5rem 1rem;
        }

        .ideas-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .empty-state {
            padding: 2rem 1rem;
        }

        .empty-icon {
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
        }

        .empty-title {
            font-size: 1.1rem;
        }

        .empty-description {
            font-size: 0.9rem;
        }
    }
</style>
