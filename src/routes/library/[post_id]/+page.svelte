<script>
    // @ts-nocheck
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    
    $: postId = $page.params.post_id;
    

    // Chart variables for performance over time
    let chartCanvas;
    let chart = null;

    // Chart variables for engagement breakdown
    let pieChartCanvas;
    let pieChart = null;

    // Chart variables for conversion rate breakdown
    let conversionChartCanvas;
    let conversionChart = null;

    // Chart variables for sentiment chart
    let sentimentChartCanvas;
    let sentimentChart = null;

    // Data variables
    let postData = null;
    let channelData = null;
    let conversionData = null;
    let sentimentData = null;

    // Data processing functions for real API data (ready for when API is available)
    function processPostData(xData, instagramData, facebookData) {
        // Process individual post metrics from multiple platforms
        const totalEngagement = (xData.engagement || 0) + (instagramData.engagement || 0) + (facebookData.engagement || 0);
        const totalReach = (xData.reach || 0) + (instagramData.reach || 0) + (facebookData.reach || 0);
        const totalImpressions = (xData.impressions || 0) + (instagramData.impressions || 0) + (facebookData.impressions || 0);
        
        return {
            title: xData.title || instagramData.title || facebookData.title || "Post Title",
            description: xData.description || instagramData.description || facebookData.description || "Post description",
            image: xData.image || instagramData.image || facebookData.image || "/api/placeholder/300/200",
            metrics: {
                engagement: { value: totalEngagement, change: calculateChange(totalEngagement, 'engagement') },
                reach: { value: totalReach, change: calculateChange(totalReach, 'reach') },
                impressions: { value: totalImpressions, change: calculateChange(totalImpressions, 'impressions') }
            },
            engagementRate: { 
                value: totalReach > 0 ? ((totalEngagement / totalReach) * 100).toFixed(1) : 0, 
                change: 0.8 
            },
            comments: (xData.comments || 0) + (instagramData.comments || 0) + (facebookData.comments || 0),
            shares: (xData.shares || 0) + (instagramData.shares || 0) + (facebookData.shares || 0)
        };
    }

    function processChannelBreakdown(xData, instagramData, facebookData) {
        const total = (xData.engagement || 0) + (instagramData.engagement || 0) + (facebookData.engagement || 0);
        if (total === 0) return { Instagram: 0, Facebook: 0, Twitter: 0, LinkedIn: 0, TikTok: 0 };
        
        return {
            Instagram: Math.round(((instagramData.engagement || 0) / total) * 100),
            Facebook: Math.round(((facebookData.engagement || 0) / total) * 100),
            Twitter: Math.round(((xData.engagement || 0) / total) * 100),
            LinkedIn: 0, // Add when LinkedIn API is available
            TikTok: 0   // Add when TikTok API is available
        };
    }

    function processConversionData(xData, instagramData, facebookData) {
        // Process conversion actions from click tracking and UTM parameters
        const purchases = (xData.conversions?.purchase || 0) + (instagramData.conversions?.purchase || 0) + (facebookData.conversions?.purchase || 0);
        const signups = (xData.conversions?.signup || 0) + (instagramData.conversions?.signup || 0) + (facebookData.conversions?.signup || 0);
        const downloads = (xData.conversions?.download || 0) + (instagramData.conversions?.download || 0) + (facebookData.conversions?.download || 0);
        const newsletter = (xData.conversions?.newsletter || 0) + (instagramData.conversions?.newsletter || 0) + (facebookData.conversions?.newsletter || 0);
        
        const total = purchases + signups + downloads + newsletter;
        if (total === 0) return { Purchase: 0, Signup: 0, Download: 0, Newsletter: 0 };
        
        return {
            Purchase: Math.round((purchases / total) * 100),
            Signup: Math.round((signups / total) * 100),
            Download: Math.round((downloads / total) * 100),
            Newsletter: Math.round((newsletter / total) * 100)
        };
    }

    function processSentimentData(xData, instagramData, facebookData) {
        // Process AI sentiment analysis from comments and interactions
        const sentiments = [xData.sentiment, instagramData.sentiment, facebookData.sentiment].filter(Boolean);
        if (sentiments.length === 0) return { Positive: 0, Neutral: 0, Negative: 0 };
        
        const avgPositive = sentiments.reduce((sum, s) => sum + (s.positive || 0), 0) / sentiments.length;
        const avgNeutral = sentiments.reduce((sum, s) => sum + (s.neutral || 0), 0) / sentiments.length;
        const avgNegative = sentiments.reduce((sum, s) => sum + (s.negative || 0), 0) / sentiments.length;
        
        return {
            Positive: Math.round(avgPositive),
            Neutral: Math.round(avgNeutral),
            Negative: Math.round(avgNegative)
        };
    }

    function calculateChange(currentValue, metricType) {
        // Calculate percentage change from previous period
        // This would use historical data from your API
        return Math.floor(Math.random() * 20) + 5; // Placeholder - replace with real calculation
    }

    // Fetch all analytics for this post using same API structure as AnalyticsDashboard
    async function fetchPostAnalytics(postId) {
        try {
            // Use same API endpoints as dashboard but with post-specific parameters
            // const xResponse = await fetch(`http://127.0.0.1:8000/api/x/posts/${postId}/analytics`);
            // const instagramResponse = await fetch(`http://127.0.0.1:8000/api/instagram/posts/${postId}/analytics`);
            // const facebookResponse = await fetch(`http://127.0.0.1:8000/api/facebook/posts/${postId}/analytics`);
            
            // const xData = await xResponse.json();
            // const instagramData = await instagramResponse.json();
            // const facebookData = await facebookData.json();

            // Process real API data when available
            // postData = processPostData(xData, instagramData, facebookData);
            // channelData = processChannelBreakdown(xData, instagramData, facebookData);
            // conversionData = processConversionData(xData, instagramData, facebookData);
            // sentimentData = processSentimentData(xData, instagramData, facebookData);

        } catch (err) {
            console.log('Using dummy data for post analytics');
        }
        
        // Using dummy data for now - aligned with dashboard values but post-specific
        postData = {
            title: "Summer Product Launch Campaign",
            description: "Introducing our latest collection with vibrant summer colors and sustainable materials. This campaign focuses on eco-friendly fashion choices for the conscious consumer.",
            image: "/api/placeholder/300/200",
            metrics: {
                engagement: { value: 8234, change: 15 },
                reach: { value: 125340, change: 12 },
                impressions: { value: 147200, change: 18 }
            },
            engagementRate: { value: 6.6, change: 0.8 },
            comments: 142,
            shares: 89
        };
        channelData = {
            Instagram: 45,
            Facebook: 25,
            Twitter: 15,
            LinkedIn: 10,
            TikTok: 5
        };
        conversionData = {
            Purchase: 40,
            Signup: 35,
            "Download": 15,
            "Newsletter": 10
        };
        sentimentData = {
            Positive: 65,
            Neutral: 25,
            Negative: 10
        };
    }

    // Fetch data when postId changes
    $: fetchPostAnalytics(postId);
    
    onMount(() => {
        // Wait for Chart.js to load, then initialize
        setTimeout(() => {
            initPerformanceChart();
            initEngagementPieChart();
            initConversionPieChart();
            initSentimentChart();
        }, 100);
    });
    
    function initPerformanceChart() {
        if (chartCanvas && typeof Chart !== 'undefined') {
            const ctx = chartCanvas.getContext('2d');
            
            // Post performance timeline - shows engagement rate from post publish to current
            // API endpoint: GET /api/posts/${postId}/performance-timeline
            // Would return: { timestamps: [], engagement_rates: [], reach_data: [], impression_data: [] }
            const data = [4.2, 4.8, 5.1, 5.9, 6.2, 6.1, 6.4, 6.3, 6.5, 6.7, 6.4, 6.6];
            const labels = ['Day 1', '', '', '', 'Day 5', '', '', '', 'Day 9', '', '', 'Current'];
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        borderColor: '#3B82F6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#3B82F6',
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#3B82F6',
                            borderWidth: 1,
                            cornerRadius: 8,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    return `Engagement Rate: ${context.parsed.y}%`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: { display: false },
                            ticks: { 
                                color: '#9CA3AF',
                                font: { size: 12 }
                            },
                            border: { display: false }
                        },
                        y: {
                            display: false,
                            grid: { display: false },
                            border: { display: false }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        } else {
            setTimeout(initPerformanceChart, 100);
        }
    }
    
    function initEngagementPieChart() {
        if (pieChartCanvas && typeof Chart !== 'undefined') {
            const ctx = pieChartCanvas.getContext('2d');
            
            // Channel engagement breakdown using same API pattern as dashboard
            // API endpoint: GET /api/posts/${postId}/channels
            // Would return: { instagram: {engagement: 123}, facebook: {engagement: 89}, twitter: {engagement: 45} }
            const labels = Object.keys(channelData);
            const data = Object.values(channelData);
            const colors = [
                '#E1306C', // Instagram pink
                '#1877F2', // Facebook blue
                '#1DA1F2', // Twitter blue
                '#0077B5', // LinkedIn blue
                '#FF0050'  // TikTok red
            ];
            
            pieChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderWidth: 2,
                        borderColor: '#ffffff',
                        hoverBorderWidth: 3,
                        hoverBorderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#3B82F6',
                            borderWidth: 1,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${percentage}%`;
                                }
                            }
                        }
                    },
                    cutout: '60%',
                    interaction: {
                        intersect: false
                    }
                }
            });
        } else {
            setTimeout(initEngagementPieChart, 100);
        }
    }
    
    function initConversionPieChart() {
        if (conversionChartCanvas && typeof Chart !== 'undefined') {
            const ctx = conversionChartCanvas.getContext('2d');
            
            // Conversion actions breakdown using UTM tracking and analytics
            // API endpoint: GET /api/posts/${postId}/conversions  
            // Would return: { purchase: 120, signup: 89, download: 45, newsletter: 23 }
            const labels = Object.keys(conversionData);
            const data = Object.values(conversionData);
            const colors = [
                '#10B981', // Purchase - Green
                '#3B82F6', // Signup - Blue
                '#8B5CF6', // Download - Purple
                '#F59E0B'  // Newsletter - Orange
            ];
            
            conversionChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderWidth: 2,
                        borderColor: '#ffffff',
                        hoverBorderWidth: 3,
                        hoverBorderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#3B82F6',
                            borderWidth: 1,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${percentage}%`;
                                }
                            }
                        }
                    },
                    cutout: '60%',
                    interaction: {
                        intersect: false
                    }
                }
            });
        } else {
            setTimeout(initConversionPieChart, 100);
        }
    }

    function initSentimentChart() {
        if (sentimentChartCanvas && typeof Chart !== 'undefined') {
            const ctx = sentimentChartCanvas.getContext('2d');
            
            // AI-powered sentiment analysis from comments and interactions
            // API endpoint: GET /api/posts/${postId}/sentiment
            // Would return: { positive: 65, neutral: 25, negative: 10, insights: [...] }
            const labels = Object.keys(sentimentData);
            const data = Object.values(sentimentData);
            const colors = [
                '#10B981', // Positive - Green
                '#6B7280', // Neutral - Gray
                '#EF4444'  // Negative - Red
            ];
            
            sentimentChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        backgroundColor: colors,
                        borderWidth: 2,
                        borderColor: '#ffffff',
                        hoverBorderWidth: 3,
                        hoverBorderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.8)',
                            titleColor: '#ffffff',
                            bodyColor: '#ffffff',
                            borderColor: '#3B82F6',
                            borderWidth: 1,
                            cornerRadius: 8,
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${percentage}%`;
                                }
                            }
                        }
                    },
                    cutout: '60%',
                    interaction: {
                        intersect: false
                    }
                }
            });
        } else {
            setTimeout(initSentimentChart, 100);
        }
    }

    // Function to navigate back to PublishedPost page
    function goBackToPublishedPosts() {
        goto('/library');
    }
</script>

<div class="post-details-container">
    <!-- Breadcrumb Navigation -->
    <nav class="breadcrumb-nav">
        <button type="button" on:click={goBackToPublishedPosts} class="breadcrumb-btn">
            <i class="fas fa-arrow-left me-2"></i>
            Back to Posts
        </button>
    </nav>
    
    <!-- Enhanced Page Header -->
    <div class="page-header">
        <div class="header-content">
            <div class="header-icon">
                <i class="fas fa-chart-line"></i>
            </div>
            <div>
                <h1 class="page-title">Post Performance</h1>
                <p class="page-subtitle">Detailed analytics and insights for your social media post</p>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Post Preview Card -->
    <div class="post-preview-card">
        <div class="card-header">
            <div class="header-icon-small">
                <i class="fas fa-file-alt"></i>
            </div>
            <h3 class="card-title">Post Preview</h3>
        </div>
        <div class="card-body">
            <div class="post-content">
                <div class="post-media">
                    <div class="media-placeholder">
                        <div class="media-icon">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="media-text">
                            <div class="media-label">YOUR</div>
                            <div class="media-label">IMAGE</div>
                        </div>
                    </div>
                </div>
                <div class="post-details">
                    <h4 class="post-title">{postData.title}</h4>
                    <p class="post-description">{postData.description}</p>
                    <div class="post-meta">
                        <span class="meta-item">
                            <i class="fas fa-calendar-alt me-1"></i>
                            Published Today
                        </span>
                        <span class="meta-item">
                            <i class="fas fa-users me-1"></i>
                            {postData.metrics.reach.value.toLocaleString()} reached
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Key Metrics -->
    <div class="metrics-section">
        <div class="section-header">
            <div class="header-icon-small">
                <i class="fas fa-chart-bar"></i>
            </div>
            <h3 class="section-title">Key Performance Metrics</h3>
        </div>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-icon engagement">
                    <i class="fas fa-heart"></i>
                </div>
                <div class="metric-content">
                    <div class="metric-label">Total Engagement</div>
                    <div class="metric-value">{postData.metrics.engagement.value.toLocaleString()}</div>
                    <div class="metric-change positive">
                        <i class="fas fa-arrow-up me-1"></i>
                        +{postData.metrics.engagement.change}% from yesterday
                    </div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon reach">
                    <i class="fas fa-users"></i>
                </div>
                <div class="metric-content">
                    <div class="metric-label">Total Reach</div>
                    <div class="metric-value">{postData.metrics.reach.value.toLocaleString()}</div>
                    <div class="metric-change positive">
                        <i class="fas fa-arrow-up me-1"></i>
                        +{postData.metrics.reach.change}% from yesterday
                    </div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon impressions">
                    <i class="fas fa-eye"></i>
                </div>
                <div class="metric-content">
                    <div class="metric-label">Total Impressions</div>
                    <div class="metric-value">{postData.metrics.impressions.value.toLocaleString()}</div>
                    <div class="metric-change positive">
                        <i class="fas fa-arrow-up me-1"></i>
                        +{postData.metrics.impressions.change}% from yesterday
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Performance Over Time -->
    <div class="chart-section">
        <div class="chart-card">
            <div class="card-header">
                <div class="header-icon-small">
                    <i class="fas fa-chart-area"></i>
                </div>
                <div class="header-content">
                    <h3 class="card-title">Performance Over Time</h3>
                    <p class="card-subtitle">Track engagement trends since publication</p>
                </div>
            </div>
            <div class="card-body">
                <div class="engagement-summary">
                    <div class="summary-item">
                        <div class="summary-label">Current Engagement Rate</div>
                        <div class="summary-value">{postData.engagementRate.value}%</div>
                        <div class="summary-change positive">
                            <i class="fas fa-trending-up me-1"></i>
                            +{postData.engagementRate.change}% from last 30 days
                        </div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <canvas bind:this={chartCanvas}></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Engagement by Channel -->
    <div class="chart-section">
        <div class="chart-card">
            <div class="card-header">
                <div class="header-icon-small">
                    <i class="fas fa-share-alt"></i>
                </div>
                <div class="header-content">
                    <h3 class="card-title">Engagement by Channel</h3>
                    <p class="card-subtitle">Platform performance breakdown for this post</p>
                </div>
            </div>
            <div class="card-body">
                <div class="chart-layout">
                    <div class="chart-container-pie">
                        <canvas bind:this={pieChartCanvas}></canvas>
                    </div>
                    <div class="chart-legend">
                        {#each Object.entries(channelData) as [channel, percentage], index}
                            <div class="legend-item">
                                <div class="legend-indicator" style="background-color: {['#E1306C', '#1877F2', '#1DA1F2', '#0077B5', '#FF0050'][index]};"></div>
                                <div class="legend-content">
                                    <span class="legend-label">{channel}</span>
                                    <span class="legend-value">{percentage}%</span>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Conversion Rate Breakdown -->
    <div class="chart-section">
        <div class="chart-card">
            <div class="card-header">
                <div class="header-icon-small">
                    <i class="fas fa-funnel-dollar"></i>
                </div>
                <div class="header-content">
                    <h3 class="card-title">Conversion Analytics</h3>
                    <p class="card-subtitle">Visitor actions and conversion performance</p>
                </div>
            </div>
            <div class="card-body">
                <div class="conversion-summary">
                    <div class="summary-item">
                        <div class="summary-label">Overall Conversion Rate</div>
                        <div class="summary-value">3.2%</div>
                        <div class="summary-change positive">
                            <i class="fas fa-arrow-up me-1"></i>
                            +0.8% from last month
                        </div>
                    </div>
                </div>
                
                <div class="chart-layout">
                    <div class="chart-container-pie">
                        <canvas bind:this={conversionChartCanvas}></canvas>
                    </div>
                    <div class="chart-legend">
                        {#each Object.entries(conversionData) as [action, percentage], index}
                            <div class="legend-item">
                                <div class="legend-indicator" style="background-color: {['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B'][index]};"></div>
                                <div class="legend-content">
                                    <span class="legend-label">{action}</span>
                                    <span class="legend-value">{percentage}%</span>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Enhanced Sentiment Detection -->
    <div class="chart-section">
        <div class="chart-card">
            <div class="card-header">
                <div class="header-icon-small">
                    <i class="fas fa-brain"></i>
                </div>
                <div class="header-content">
                    <h3 class="card-title">AI Sentiment Analysis</h3>
                    <p class="card-subtitle">Audience emotions and reaction insights</p>
                </div>
            </div>
            <div class="card-body">
                <div class="sentiment-summary">
                    <div class="summary-item">
                        <div class="summary-label">Overall Sentiment Score</div>
                        <div class="summary-value sentiment-positive">7.8/10</div>
                        <div class="summary-change positive">
                            <i class="fas fa-smile me-1"></i>
                            Predominantly positive audience reaction
                        </div>
                    </div>
                </div>
                
                <div class="chart-layout">
                    <div class="chart-container-pie">
                        <canvas bind:this={sentimentChartCanvas}></canvas>
                    </div>
                    <div class="sentiment-insights">
                        {#each Object.entries(sentimentData) as [sentiment, percentage], index}
                            <div class="legend-item">
                                <div class="legend-indicator" style="background-color: {['#10B981', '#6B7280', '#EF4444'][index]};"></div>
                                <div class="legend-content">
                                    <span class="legend-label">{sentiment}</span>
                                    <span class="legend-value">{percentage}%</span>
                                </div>
                            </div>
                        {/each}
                        
                        <!-- Enhanced insights -->
                        <div class="insights-section">
                            <h6 class="insights-title">
                                <i class="fas fa-lightbulb me-2"></i>
                                Key Insights
                            </h6>
                            <div class="insight-item positive">
                                <i class="fas fa-heart"></i>
                                High positive engagement from younger demographics
                            </div>
                            <div class="insight-item info">
                                <i class="fas fa-comment-dots"></i>
                                Comments mention product quality and value
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</div>

<style>
    /* Main Container */
    .post-details-container {
        background: transparent;
        min-height: 100vh;
        padding: 2rem;
    }

    /* Breadcrumb Navigation - Outside container */
    .breadcrumb-nav {
        margin-bottom: 2rem;
    }

    .breadcrumb-btn {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #667eea;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
    }

    .breadcrumb-btn:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }

    /* Enhanced Page Header */
    .page-header {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .header-content {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .header-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.8rem;
        flex-shrink: 0;
    }

    .page-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 2rem;
        line-height: 1.2;
    }

    .page-subtitle {
        margin: 0.5rem 0 0 0;
        color: #718096;
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* Enhanced Post Preview Card */
    .post-preview-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin-bottom: 2rem;
    }

    .card-header {
        padding: 1.5rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .header-icon-small {
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
        font-size: 1.3rem;
    }

    .card-body {
        padding: 2rem;
    }

    .post-content {
        display: grid;
        grid-template-columns: 1fr 2fr;
        gap: 2rem;
        align-items: start;
    }

    .post-media {
        position: relative;
    }

    .media-placeholder {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-radius: 15px;
        padding: 3rem 2rem;
        text-align: center;
        border: 2px dashed rgba(102, 126, 234, 0.3);
    }

    .media-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        margin: 0 auto 1rem;
    }

    .media-label {
        color: #667eea;
        font-weight: 700;
        font-size: 1.1rem;
        line-height: 1.2;
    }

    .post-details {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .post-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        margin: 0;
        line-height: 1.3;
    }

    .post-description {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }

    .post-meta {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
    }

    .meta-item {
        display: flex;
        align-items: center;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Enhanced Metrics Section */
    .metrics-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
        margin-bottom: 2rem;
    }

    .section-header {
        padding: 1.5rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .section-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        padding: 2rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
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

    .metric-card:hover::before {
        opacity: 1;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .metric-card > * {
        position: relative;
        z-index: 2;
    }

    .metric-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }

    .metric-icon.engagement {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }

    .metric-icon.reach {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }

    .metric-icon.impressions {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }

    .metric-content {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .metric-label {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .metric-value {
        color: #2d3748;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
    }

    .metric-change {
        display: flex;
        align-items: center;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .metric-change.positive {
        color: #10b981;
    }

    /* Enhanced Chart Sections */
    .chart-section {
        margin-bottom: 2rem;
    }

    .chart-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .card-subtitle {
        margin: 0.25rem 0 0 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .engagement-summary,
    .conversion-summary,
    .sentiment-summary {
        padding: 1.5rem 2rem;
        background: rgba(102, 126, 234, 0.02);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }

    .summary-item {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .summary-label {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .summary-value {
        color: #2d3748;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
    }

    .summary-value.sentiment-positive {
        color: #10b981;
    }

    .summary-change {
        display: flex;
        align-items: center;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .summary-change.positive {
        color: #10b981;
    }

    .chart-container {
        height: 350px;
        position: relative;
        padding: 2rem;
    }

    .chart-layout {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        align-items: center;
        padding: 2rem;
    }

    .chart-container-pie {
        height: 300px;
        position: relative;
    }

    .chart-legend,
    .sentiment-insights {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }

    .legend-item:hover {
        background: rgba(102, 126, 234, 0.05);
        transform: translateX(5px);
    }

    .legend-indicator {
        width: 16px;
        height: 16px;
        border-radius: 4px;
        flex-shrink: 0;
    }

    .legend-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex: 1;
    }

    .legend-label {
        color: #2d3748;
        font-weight: 500;
        font-size: 0.9rem;
    }

    .legend-value {
        color: #667eea;
        font-weight: 700;
        font-size: 0.9rem;
    }

    /* Enhanced Insights Section */
    .insights-section {
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }

    .insights-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }

    .insight-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 10px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .insight-item:last-child {
        margin-bottom: 0;
    }

    .insight-item.positive {
        background: rgba(16, 185, 129, 0.1);
        color: #065f46;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .insight-item.info {
        background: rgba(59, 130, 246, 0.1);
        color: #1e40af;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    .insight-item.success {
        background: rgba(34, 197, 94, 0.1);
        color: #15803d;
        border: 1px solid rgba(34, 197, 94, 0.2);
    }

    .insight-item i {
        flex-shrink: 0;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .post-details-container {
            padding: 1rem;
        }

        .page-header {
            padding: 1.5rem;
        }

        .header-content {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }

        .page-title {
            font-size: 1.5rem;
        }

        .post-content {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .metrics-grid {
            grid-template-columns: 1fr;
            padding: 1.5rem;
        }

        .chart-layout {
            grid-template-columns: 1fr;
            gap: 1.5rem;
            padding: 1.5rem;
        }

        .chart-container {
            padding: 1.5rem;
        }

        .card-body {
            padding: 1.5rem;
        }

        .engagement-summary,
        .conversion-summary,
        .sentiment-summary {
            padding: 1.5rem;
        }

        .post-meta {
            flex-direction: column;
            gap: 0.75rem;
        }

        .breadcrumb-btn {
            width: 100%;
            justify-content: center;
        }
    }

    /* Enhanced Global Canvas Styling */
    :global(canvas) {
        width: 100% !important;
        height: 100% !important;
    }
</style>