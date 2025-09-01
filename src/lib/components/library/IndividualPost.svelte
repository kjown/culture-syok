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
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 0,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#667eea',
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
                            borderColor: '#667eea',
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
                            borderColor: '#667eea',
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
                '#667eea', // Signup - Blue
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
                            borderColor: '#667eea',
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
                            borderColor: '#667eea',
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

<div class="container py-4">
    <!-- Enhanced Page Header -->
    <div class="page-header">
        <div class="breadcrumb-container">
            <button 
                type="button" 
                on:click={goBackToPublishedPosts} 
                class="breadcrumb-btn"
            >
                <i class="fas fa-arrow-left me-2"></i>
                Back to Library
            </button>
        </div>
        
        <h1 class="page-title">
            <i class="fas fa-chart-line me-3"></i>
            Post Analytics
        </h1>
        <p class="page-subtitle">Comprehensive performance insights for your social media content</p>
    </div>
    
    <!-- Post Preview Card -->
    <div class="post-preview-card">
        <div class="card-header">
            <div class="header-icon">
                <i class="fas fa-file-text"></i>
            </div>
            <div>
                <h3 class="card-title">Content Preview</h3>
                <p class="card-subtitle">Original post details and performance overview</p>
            </div>
        </div>
        
        <div class="card-content">
            <div class="post-display">
                <div class="post-image-placeholder">
                    <div class="placeholder-content">
                        <div class="placeholder-icon">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="placeholder-text">
                            <div class="placeholder-title">YOUR</div>
                            <div class="placeholder-title">IMAGE</div>
                        </div>
                    </div>
                </div>
                <div class="post-details">
                    <h3 class="post-title">{postData.title}</h3>
                    <p class="post-description">{postData.description}</p>
                    <div class="post-meta">
                        <span class="meta-item">
                            <i class="fas fa-calendar me-2"></i>
                            Published 5 days ago
                        </span>
                        <span class="meta-item">
                            <i class="fas fa-share-alt me-2"></i>
                            3 platforms
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Key Metrics Grid -->
    <div class="metrics-section">
        <div class="section-header">
            <h3 class="section-title">
                <i class="fas fa-chart-bar me-2"></i>
                Key Performance Metrics
            </h3>
            <p class="section-subtitle">Real-time engagement data across all platforms</p>
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
                        <i class="fas fa-arrow-up"></i>
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
                        <i class="fas fa-arrow-up"></i>
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
                        <i class="fas fa-arrow-up"></i>
                        +{postData.metrics.impressions.change}% from yesterday
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Performance Over Time Chart -->
    <div class="chart-card">
        <div class="chart-header">
            <div class="header-content">
                <div class="header-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
                <div>
                    <h3 class="chart-title">Performance Timeline</h3>
                    <p class="chart-subtitle">Engagement rate progression since publication</p>
                </div>
            </div>
            
            <div class="chart-stats">
                <div class="stat-item">
                    <div class="stat-label">Current Rate</div>
                    <div class="stat-value">{postData.engagementRate.value}%</div>
                </div>
                <div class="stat-change positive">
                    <i class="fas fa-trending-up"></i>
                    +{postData.engagementRate.change}% this month
                </div>
            </div>
        </div>
        
        <div class="chart-container">
            <canvas bind:this={chartCanvas}></canvas>
        </div>
    </div>
    
    <!-- Analytics Grid -->
    <div class="analytics-grid">
        <!-- Engagement by Channel -->
        <div class="analytics-card">
            <div class="analytics-header">
                <div class="header-icon">
                    <i class="fas fa-share-alt"></i>
                </div>
                <div>
                    <h3 class="analytics-title">Platform Breakdown</h3>
                    <p class="analytics-subtitle">Engagement distribution across channels</p>
                </div>
            </div>
            
            <div class="analytics-content">
                <div class="chart-section">
                    <div class="pie-chart-container">
                        <canvas bind:this={pieChartCanvas}></canvas>
                    </div>
                </div>
                
                <div class="legend-section">
                    {#each Object.entries(channelData) as [channel, percentage], index}
                        <div class="legend-item">
                            <div class="legend-color" style="background-color: {['#E1306C', '#1877F2', '#1DA1F2', '#0077B5', '#FF0050'][index]};"></div>
                            <span class="legend-label">{channel}</span>
                            <span class="legend-value">{percentage}%</span>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
        
        <!-- Conversion Analytics -->
        <div class="analytics-card">
            <div class="analytics-header">
                <div class="header-icon">
                    <i class="fas fa-bullseye"></i>
                </div>
                <div>
                    <h3 class="analytics-title">Conversion Actions</h3>
                    <p class="analytics-subtitle">User actions from this post</p>
                </div>
            </div>
            
            <div class="conversion-stats">
                <div class="conversion-summary">
                    <div class="summary-label">Overall Rate</div>
                    <div class="summary-value">3.2%</div>
                    <div class="summary-change positive">+0.8% vs last month</div>
                </div>
            </div>
            
            <div class="analytics-content">
                <div class="chart-section">
                    <div class="pie-chart-container">
                        <canvas bind:this={conversionChartCanvas}></canvas>
                    </div>
                </div>
                
                <div class="legend-section">
                    {#each Object.entries(conversionData) as [action, percentage], index}
                        <div class="legend-item">
                            <div class="legend-color" style="background-color: {['#10B981', '#667eea', '#8B5CF6', '#F59E0B'][index]};"></div>
                            <span class="legend-label">{action}</span>
                            <span class="legend-value">{percentage}%</span>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Sentiment Analysis -->
    <div class="sentiment-card">
        <div class="sentiment-header">
            <div class="header-content">
                <div class="header-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <div>
                    <h3 class="sentiment-title">AI Sentiment Analysis</h3>
                    <p class="sentiment-subtitle">Audience emotion analysis from comments and reactions</p>
                </div>
            </div>
            
            <div class="sentiment-score">
                <div class="score-container">
                    <div class="score-label">Overall Score</div>
                    <div class="score-value">7.8<span>/10</span></div>
                    <div class="score-status positive">Predominantly Positive</div>
                </div>
            </div>
        </div>
        
        <div class="sentiment-content">
            <div class="sentiment-chart">
                <div class="pie-chart-container">
                    <canvas bind:this={sentimentChartCanvas}></canvas>
                </div>
            </div>
            
            <div class="sentiment-details">
                <div class="sentiment-breakdown">
                    {#each Object.entries(sentimentData) as [sentiment, percentage], index}
                        <div class="sentiment-item">
                            <div class="sentiment-color" style="background-color: {['#10B981', '#6B7280', '#EF4444'][index]};"></div>
                            <span class="sentiment-label">{sentiment}</span>
                            <span class="sentiment-percentage">{percentage}%</span>
                        </div>
                    {/each}
                </div>
                
                <div class="sentiment-insights">
                    <div class="insights-header">
                        <i class="fas fa-lightbulb me-2"></i>
                        Key Insights
                    </div>
                    <div class="insight-list">
                        <div class="insight-item">
                            <i class="fas fa-heart text-success"></i>
                            High positive engagement from younger demographics
                        </div>
                        <div class="insight-item">
                            <i class="fas fa-comment text-info"></i>
                            Comments mention product quality and value
                        </div>
                        <div class="insight-item">
                            <i class="fas fa-trending-up text-warning"></i>
                            Sentiment improved 15% from last post
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Page Header */
    .page-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
        position: relative;
    }

    .breadcrumb-container {
        margin-bottom: 2rem;
    }

    .breadcrumb-btn {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        color: #667eea;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
    }

    .breadcrumb-btn:hover {
        background: rgba(102, 126, 234, 0.15);
        transform: translateY(-1px);
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

    /* Post Preview Card */
    .post-preview-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 3rem;
        overflow: hidden;
    }

    .card-header {
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

    .card-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .card-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .card-content {
        padding: 2rem;
    }

    .post-display {
        display: grid;
        grid-template-columns: 300px 1fr;
        gap: 2rem;
        align-items: center;
    }

    .post-image-placeholder {
        height: 200px;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid rgba(102, 126, 234, 0.1);
    }

    .placeholder-content {
        text-align: center;
    }

    .placeholder-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        margin: 0 auto 1rem;
    }

    .placeholder-title {
        font-weight: 700;
        color: #2d3748;
        font-size: 1.1rem;
    }

    .post-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }

    .post-description {
        color: #4a5568;
        line-height: 1.6;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .post-meta {
        display: flex;
        gap: 2rem;
    }

    .meta-item {
        display: flex;
        align-items: center;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .meta-item i {
        color: #667eea;
    }

    /* Metrics Section */
    .metrics-section {
        margin-bottom: 3rem;
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
    }

    .section-title i {
        color: #667eea;
    }

    .section-subtitle {
        color: #718096;
        font-size: 1rem;
        font-weight: 500;
        margin: 0;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }

    .metric-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
    }

    .metric-icon.engagement {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }

    .metric-icon.reach {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .metric-icon.impressions {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    .metric-content {
        flex: 1;
    }

    .metric-label {
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #2d3748;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .metric-change {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .metric-change.positive {
        color: #10b981;
    }

    /* Chart Cards */
    .chart-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 3rem;
        overflow: hidden;
    }

    .chart-header {
        padding: 2rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .header-content {
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .chart-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .chart-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .chart-stats {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    .stat-item {
        text-align: right;
    }

    .stat-label {
        color: #718096;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }

    .stat-value {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 700;
    }

    .stat-change {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }

    .stat-change.positive {
        color: #10b981;
    }

    .chart-container {
        padding: 2rem;
        height: 350px;
        position: relative;
    }

    /* Analytics Grid */
    .analytics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
    }

    .analytics-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .analytics-header {
        padding: 1.5rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .analytics-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
    }

    .analytics-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .analytics-content {
        padding: 2rem;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        align-items: center;
    }

    .chart-section {
        display: flex;
        justify-content: center;
    }

    .pie-chart-container {
        height: 250px;
        width: 250px;
        position: relative;
    }

    .legend-section {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .legend-label {
        flex: 1;
        color: #4a5568;
        font-weight: 500;
        font-size: 0.9rem;
    }

    .legend-value {
        color: #2d3748;
        font-weight: 600;
        font-size: 0.9rem;
    }

    /* Conversion Stats */
    .conversion-stats {
        padding: 1.5rem 2rem 0;
    }

    .conversion-summary {
        text-align: center;
        padding: 1rem;
        background: rgba(102, 126, 234, 0.05);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    .summary-label {
        color: #718096;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .summary-value {
        color: #2d3748;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .summary-change {
        color: #10b981;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* Sentiment Card */
    .sentiment-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .sentiment-header {
        padding: 2rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .sentiment-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .sentiment-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .sentiment-score {
        text-align: center;
    }

    .score-container {
        background: rgba(16, 185, 129, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .score-label {
        color: #718096;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .score-value {
        color: #10b981;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .score-value span {
        font-size: 1.2rem;
        opacity: 0.7;
    }

    .score-status {
        color: #10b981;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .sentiment-content {
        padding: 2rem;
        display: grid;
        grid-template-columns: 300px 1fr;
        gap: 3rem;
        align-items: start;
    }

    .sentiment-chart {
        display: flex;
        justify-content: center;
    }

    .sentiment-details {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }

    .sentiment-breakdown {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .sentiment-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem 0;
    }

    .sentiment-color {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .sentiment-label {
        flex: 1;
        color: #4a5568;
        font-weight: 500;
        font-size: 0.95rem;
    }

    .sentiment-percentage {
        color: #2d3748;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .sentiment-insights {
        background: rgba(102, 126, 234, 0.02);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .insights-header {
        color: #2d3748;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }

    .insights-header i {
        color: #667eea;
    }

    .insight-list {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .insight-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #4a5568;
        font-size: 0.9rem;
        line-height: 1.4;
    }

    .insight-item i {
        width: 16px;
        flex-shrink: 0;
    }

    /* Responsive Design */
    @media (max-width: 1200px) {
        .analytics-grid {
            grid-template-columns: 1fr;
        }
        
        .sentiment-content {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
    }

    @media (max-width: 768px) {
        .container {
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

        .post-display {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }

        .post-image-placeholder {
            height: 150px;
        }

        .metrics-grid {
            grid-template-columns: 1fr;
        }

        .metric-card {
            padding: 1.5rem;
        }

        .chart-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            gap: 1rem;
            text-align: center;
        }

        .chart-stats {
            gap: 1rem;
        }

        .chart-container {
            padding: 1.5rem 1rem;
            height: 300px;
        }

        .analytics-content {
            grid-template-columns: 1fr;
            padding: 1.5rem;
        }

        .legend-section {
            margin-top: 1rem;
        }

        .sentiment-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            gap: 1rem;
        }

        .sentiment-content {
            padding: 1.5rem 1rem;
        }
    }
</style>    