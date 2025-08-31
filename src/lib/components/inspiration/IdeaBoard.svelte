<script>
    import GeneratedIdeaCard from "./GeneratedIdeaCard.svelte";

    /**
     * @typedef {Object} IdeaItem
     * @property {string} title
     * @property {string} description
     * @property {string[]} tags
     * @property {string} intent
     */

    /** @type {Record<string, IdeaItem[]>} */
    const ideas = {
        "New Ideas": [
            {
                title: "Repurpose Blog Posts for Social Media",
                description:
                    "Turn your old blog posts into engaging social media content.",
                tags: ["Content Creation", "Social Media"],
                intent: "Inform",
            },
            {
                title: "Weekly Marketing Tip",
                description:
                    "Share a quick marketing tip every week to boost engagement.",
                tags: ["Marketing", "Tips"],
                intent: "Describe",
            },
        ],
        Drafting: [
            {
                title: "Draft: Instagram Carousel on Trends",
                description: "A carousel post about the latest digital trends.",
                tags: ["Social Media", "Trends"],
                intent: "Tell A Story",
            },
        ],
        "Ready to Schedule": [
            {
                title: "Scheduled: Email Newsletter",
                description:
                    "Monthly newsletter ready to be sent to subscribers.",
                tags: ["Email", "Newsletter"],
                intent: "Inform",
            },
        ],
    };

    let activeTab = "New Ideas";
    let tabs = Object.keys(ideas);
</script>

<div class="idea-board">
    <div class="board-header">
        <div class="header-icon">
            <i class="fas fa-clipboard-list"></i>
        </div>
        <div>
            <h2 class="board-title">Idea Board</h2>
            <p class="board-subtitle">Organize and manage your content ideas through different stages</p>
        </div>
    </div>

    <div class="board-content">
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
                        <span class="tab-count">({ideas[tab].length})</span>
                    </div>
                    {#if tab === "New Ideas"}
                        <i class="fas fa-plus-circle tab-icon"></i>
                    {:else if tab === "Drafting"}
                        <i class="fas fa-edit tab-icon"></i>
                    {:else if tab === "Ready to Schedule"}
                        <i class="fas fa-calendar-check tab-icon"></i>
                    {/if}
                </button>
            {/each}
        </div>

        <!-- Tab Content -->
        <div class="tab-content-area">
            <div class="ideas-container">
                {#each ideas[activeTab] as idea}
                    <GeneratedIdeaCard {idea} />
                {/each}
                {#if ideas[activeTab].length === 0}
                    <div class="empty-state">
                        <div class="empty-icon">
                            {#if activeTab === "New Ideas"}
                                <i class="fas fa-lightbulb"></i>
                            {:else if activeTab === "Drafting"}
                                <i class="fas fa-pen-nib"></i>
                            {:else}
                                <i class="fas fa-calendar-alt"></i>
                            {/if}
                        </div>
                        <h4 class="empty-title">No ideas in {activeTab.toLowerCase()} yet</h4>
                        <p class="empty-description">
                            {#if activeTab === "New Ideas"}
                                Generate some creative ideas using our AI tool above!
                            {:else if activeTab === "Drafting"}
                                Move ideas here when you're ready to start working on them.
                            {:else}
                                Ideas that are polished and ready to be scheduled will appear here.
                            {/if}
                        </p>
                        <button class="empty-action-btn">
                            <i class="fas fa-plus"></i>
                            {#if activeTab === "New Ideas"}
                                Generate Ideas
                            {:else if activeTab === "Drafting"}
                                Start Drafting
                            {:else}
                                Schedule Content
                            {/if}
                        </button>
                    </div>
                {/if}
            </div>
        </div>
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
        margin-bottom: 2rem;
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

    .board-content {
        padding: 2rem;
    }

    .tab-navigation {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 2rem;
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

    .tab-content-area {
        min-height: 300px;
    }

    .ideas-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #718096;
        grid-column: 1 / -1;
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
    @media (max-width: 768px) {
        .board-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            text-align: center;
        }

        .board-content {
            padding: 1.5rem 1rem;
        }

        .tab-navigation {
            flex-direction: column;
            gap: 0.5rem;
        }

        .tab-btn {
            padding: 0.875rem 1rem;
        }

        .ideas-container {
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
