<script>
    import { goto } from "$app/navigation";

    let posts = [
        {
            id: "1",
            content:
                "Check out my latest blog post on sustainable living! #ecofriendly #sustainability",
            channel: "Blog",
            published: "2023-08-15",
            impressions: 1200,
            likes: 50,
            comments: 10,
            shares: 5,
        },
        {
            id: "2",
            content:
                "Just finished a great workout! Feeling energized and ready to tackle the day. #fitness #healthylifestyle",
            channel: "Instagram",
            published: "2023-08-14",
            impressions: 1500,
            likes: 75,
            comments: 15,
            shares: 8,
        },
        {
            id: "3",
            content:
                "Excited to announce our new partnership with GreenTech Solutions! Together, we'll be working towards a greener future. #collaboration #innovation",
            channel: "LinkedIn",
            published: "2023-08-13",
            impressions: 1800,
            likes: 90,
            comments: 20,
            shares: 10,
        },
        {
            id: "4",
            content:
                "Happy Friday everyone! What are your plans for the weekend? #weekendvibes #friyay",
            channel: "Twitter",
            published: "2023-08-12",
            impressions: 2000,
            likes: 100,
            comments: 25,
            shares: 12,
        },
        {
            id: "5",
            content:
                "Throwback to our team retreat last month. Such a fun and productive time! #teamwork #retreat",
            channel: "Facebook",
            published: "2023-08-11",
            impressions: 2200,
            likes: 110,
            comments: 30,
            shares: 15,
        },
    ];

    let search = "";
    let selectedChannel = "Channel";
    let selectedDate = "Date Range";
    let selectedSort = "Sort";
    let channels = [
        "Channel",
        "Blog",
        "Instagram",
        "LinkedIn",
        "Twitter",
        "Facebook",
    ];
    let dateRanges = [
        "Date Range",
        "Last 7 days",
        "Last 30 days",
        "Last 90 days",
    ];
    let sortOptions = [
        "Sort",
        "Newest",
        "Oldest",
        "Most Impressions",
        "Most Likes",
    ];

    /**
     * @param {string} id
     */
    function viewPost(id) {
        goto(`/library/${id}`);
    }
</script>

<div class="library-container">
    <!-- Enhanced Page Header -->
    <div class="page-header">
        <h1 class="page-title">
            <i class="fas fa-archive me-3"></i>
            Published Posts
        </h1>
        <p class="page-subtitle">Track and analyze the performance of your published content across all platforms</p>
    </div>

    <!-- Enhanced Filters Section -->
    <div class="filters-section">
        <div class="search-container">
            <div class="search-wrapper">
                <i class="fas fa-search search-icon"></i>
                <input
                    class="search-input"
                    type="search"
                    placeholder="Search your published posts..."
                    bind:value={search}
                />
            </div>
        </div>

        <div class="filter-controls">
            <div class="filter-item">
                <label class="filter-label">
                    <i class="fas fa-filter me-2"></i>
                    Channel
                </label>
                <select class="filter-select" bind:value={selectedChannel}>
                    {#each channels as channel}
                        <option value={channel}>{channel}</option>
                    {/each}
                </select>
            </div>
            
            <div class="filter-item">
                <label class="filter-label">
                    <i class="fas fa-calendar me-2"></i>
                    Date Range
                </label>
                <select class="filter-select" bind:value={selectedDate}>
                    {#each dateRanges as range}
                        <option value={range}>{range}</option>
                    {/each}
                </select>
            </div>
            
            <div class="filter-item">
                <label class="filter-label">
                    <i class="fas fa-sort me-2"></i>
                    Sort By
                </label>
                <select class="filter-select" bind:value={selectedSort}>
                    {#each sortOptions as sort}
                        <option value={sort}>{sort}</option>
                    {/each}
                </select>
            </div>
        </div>
    </div>

    <!-- Enhanced Posts Table -->
    <div class="posts-table-container">
        <div class="table-header">
            <h3 class="table-title">
                <i class="fas fa-list me-2"></i>
                Posts Library
            </h3>
            <span class="posts-count">{posts.length} posts found</span>
        </div>
        
        <div class="table-wrapper">
            <table class="posts-table">
                <thead>
                    <tr>
                        <th class="post-column">
                            <i class="fas fa-file-text me-2"></i>
                            Content
                        </th>
                        <th class="channel-column">
                            <i class="fas fa-share-alt me-2"></i>
                            Platform
                        </th>
                        <th class="date-column">
                            <i class="fas fa-calendar-alt me-2"></i>
                            Published
                        </th>
                        <th class="metric-column">
                            <i class="fas fa-eye me-2"></i>
                            Impressions
                        </th>
                        <th class="metric-column">
                            <i class="fas fa-heart me-2"></i>
                            Likes
                        </th>
                        <th class="metric-column">
                            <i class="fas fa-comment me-2"></i>
                            Comments
                        </th>
                        <th class="metric-column">
                            <i class="fas fa-share me-2"></i>
                            Shares
                        </th>
                        <th class="actions-column">
                            <i class="fas fa-cog me-2"></i>
                            Actions
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {#each posts as post}
                        <tr class="post-row">
                            <td class="post-content">
                                <div class="content-wrapper">
                                    <p class="content-text">{post.content}</p>
                                    <div class="content-preview">
                                        {post.content.substring(0, 100)}{post.content.length > 100 ? '...' : ''}
                                    </div>
                                </div>
                            </td>
                            <td class="channel-cell">
                                <div class="channel-badge {post.channel.toLowerCase()}">
                                    {#if post.channel === 'Instagram'}
                                        <i class="fab fa-instagram"></i>
                                    {:else if post.channel === 'Facebook'}
                                        <i class="fab fa-facebook"></i>
                                    {:else if post.channel === 'Twitter'}
                                        <i class="fab fa-x-twitter"></i>
                                    {:else if post.channel === 'LinkedIn'}
                                        <i class="fab fa-linkedin"></i>
                                    {:else}
                                        <i class="fas fa-globe"></i>
                                    {/if}
                                    <span>{post.channel}</span>
                                </div>
                            </td>
                            <td class="date-cell">
                                <span class="date-text">{post.published}</span>
                            </td>
                            <td class="metric-cell">
                                <span class="metric-value impressions">{post.impressions.toLocaleString()}</span>
                            </td>
                            <td class="metric-cell">
                                <span class="metric-value likes">{post.likes}</span>
                            </td>
                            <td class="metric-cell">
                                <span class="metric-value comments">{post.comments}</span>
                            </td>
                            <td class="metric-cell">
                                <span class="metric-value shares">{post.shares}</span>
                            </td>
                            <td class="actions-cell">
                                <button
                                    class="action-btn view-btn"
                                    type="button"
                                    on:click={() => viewPost(post.id)}
                                >
                                    <i class="fas fa-chart-line me-2"></i>
                                    View Analytics
                                </button>
                            </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    </div>
</div>

<style>
    .library-container {
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

    /* Filters Section */
    .filters-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .search-container {
        margin-bottom: 1.5rem;
    }

    .search-wrapper {
        position: relative;
        max-width: 500px;
        margin: 0 auto;
    }

    .search-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #9ca3af;
        font-size: 1rem;
    }

    .search-input {
        width: 100%;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1rem 1rem 3rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }

    .search-input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
        background: rgba(255, 255, 255, 0.95);
    }

    .filter-controls {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }

    .filter-item {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .filter-label {
        font-weight: 600;
        color: #2d3748;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
    }

    .filter-label i {
        color: #667eea;
    }

    .filter-select {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }

    .filter-select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }

    /* Posts Table */
    .posts-table-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .table-header {
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .table-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
        margin: 0;
        display: flex;
        align-items: center;
    }

    .table-title i {
        color: #667eea;
    }

    .posts-count {
        color: #718096;
        font-weight: 500;
        font-size: 0.9rem;
        background: rgba(102, 126, 234, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
    }

    .table-wrapper {
        overflow-x: auto;
    }

    .posts-table {
        width: 100%;
        border-collapse: collapse;
    }

    .posts-table thead {
        background: rgba(102, 126, 234, 0.03);
    }

    .posts-table th {
        padding: 1rem 1.5rem;
        text-align: left;
        font-weight: 600;
        color: #2d3748;
        font-size: 0.9rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.1);
    }

    .posts-table th i {
        color: #667eea;
        font-size: 0.8rem;
    }

    .post-row {
        transition: all 0.3s ease;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }

    .post-row:hover {
        background: rgba(102, 126, 234, 0.02);
    }

    .posts-table td {
        padding: 1.5rem 1.5rem;
        vertical-align: top;
    }

    .post-content {
        max-width: 300px;
    }

    .content-wrapper {
        position: relative;
    }

    .content-text {
        display: none;
    }

    .content-preview {
        color: #4a5568;
        line-height: 1.5;
        font-size: 0.9rem;
    }

    .channel-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        font-size: 0.85rem;
        color: #4a5568;
    }

    .date-text {
        color: #4a5568;
        font-weight: 500;
        font-size: 0.9rem;
    }

    .metric-value {
        font-weight: 600;
        font-size: 0.95rem;
        color: #4a5568;
    }

    .action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Responsive design */
    @media (max-width: 1200px) {
        .library-container {
            padding: 1.5rem 1rem;
        }

        .table-wrapper {
            overflow-x: scroll;
        }

        .posts-table {
            min-width: 1000px;
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

        .filters-section {
            padding: 1.5rem 1rem;
        }

        .filter-controls {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .table-header {
            padding: 1rem;
            flex-direction: column;
            gap: 0.5rem;
            text-align: center;
        }

        .posts-table th,
        .posts-table td {
            padding: 1rem 0.75rem;
        }

        .post-content {
            max-width: 200px;
        }

        .action-btn {
            padding: 0.6rem 1rem;
            font-size: 0.8rem;
        }
    }
</style>
