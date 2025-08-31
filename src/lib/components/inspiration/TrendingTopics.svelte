<script>
    // No props needed for static topics
</script>

<div class="trending-topics">
    <div class="section-header">
        <h5 class="section-title">
            <i class="fas fa-fire me-2"></i>
            Trending Topics
        </h5>
        <p class="section-subtitle">Discover what's popular in your industry right now</p>
    </div>
    
    <div class="topics-grid">
        <div class="topic-card">
            <div class="topic-icon">
                <span class="emoji">📰</span>
            </div>
            <div class="topic-content">
                <h6 class="topic-title">#TechNews</h6>
                <p class="topic-description">Latest tech news and updates</p>
            </div>
            <div class="topic-overlay">
                <button class="use-topic-btn">
                    <i class="fas fa-plus"></i>
                    Use Topic
                </button>
            </div>
        </div>

        <div class="topic-card">
            <div class="topic-icon">
                <span class="emoji">💡</span>
            </div>
            <div class="topic-content">
                <h6 class="topic-title">#MarketingTips</h6>
                <p class="topic-description">Marketing strategies and tips</p>
            </div>
            <div class="topic-overlay">
                <button class="use-topic-btn">
                    <i class="fas fa-plus"></i>
                    Use Topic
                </button>
            </div>
        </div>

        <div class="topic-card">
            <div class="topic-icon">
                <span class="emoji">📱</span>
            </div>
            <div class="topic-content">
                <h6 class="topic-title">#SocialMedia</h6>
                <p class="topic-description">Social media trends and insights</p>
            </div>
            <div class="topic-overlay">
                <button class="use-topic-btn">
                    <i class="fas fa-plus"></i>
                    Use Topic
                </button>
            </div>
        </div>

        <div class="topic-card">
            <div class="topic-icon">
                <span class="emoji">📝</span>
            </div>
            <div class="topic-content">
                <h6 class="topic-title">#ContentCreation</h6>
                <p class="topic-description">Content creation ideas and tools</p>
            </div>
            <div class="topic-overlay">
                <button class="use-topic-btn">
                    <i class="fas fa-plus"></i>
                    Use Topic
                </button>
            </div>
        </div>

        <div class="topic-card">
            <div class="topic-icon">
                <span class="emoji">📊</span>
            </div>
            <div class="topic-content">
                <h6 class="topic-title">#DigitalTrends</h6>
                <p class="topic-description">Digital trends and innovations</p>
            </div>
            <div class="topic-overlay">
                <button class="use-topic-btn">
                    <i class="fas fa-plus"></i>
                    Use Topic
                </button>
            </div>
        </div>
    </div>
</div>

<style>
    .trending-topics {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .section-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .section-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .section-title i {
        color: #667eea;
        font-size: 1.3rem;
    }

    .section-subtitle {
        color: #718096;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
    }

    .topics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }

    .topic-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }

    .topic-card::before {
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

    .topic-card:hover::before {
        opacity: 1;
    }

    .topic-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }

    .topic-card:hover .topic-overlay {
        opacity: 1;
    }

    .topic-icon {
        position: relative;
        z-index: 2;
        margin-bottom: 1rem;
    }

    .emoji {
        font-size: 2.5rem;
        display: inline-block;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }

    .topic-content {
        position: relative;
        z-index: 2;
    }

    .topic-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .topic-description {
        color: #718096;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.4;
    }

    .topic-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(102, 126, 234, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 3;
    }

    .use-topic-btn {
        background: white;
        color: #667eea;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }

    .use-topic-btn:hover {
        background: #f8f9ff;
        transform: scale(1.05);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .trending-topics {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .topics-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }

        .topic-card {
            padding: 1rem;
        }

        .emoji {
            font-size: 2rem;
            width: 60px;
            height: 60px;
        }

        .section-title {
            font-size: 1.3rem;
        }
    }
</style>
