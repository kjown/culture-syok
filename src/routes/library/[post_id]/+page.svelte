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

<div class="container py-4">
    <!-- Breadcrumb -->
    <nav class="mb-4">
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <button type="button" on:click={goBackToPublishedPosts} class="btn btn-link p-0 text-decoration-none text-muted" style="cursor: pointer; border: none; background: none;">Posts</button>
            </li>
            <li class="breadcrumb-item text-muted" aria-current="page">Post Details</li>
        </ol>
    </nav>
    
    <!-- Page Header -->
    <div class="mb-4">
        <h1 class="h2 mb-2">Post Performance</h1>
        <p class="text-muted">Detailed analytics for your social media post</p>
    </div>
    
    <!-- Post Preview Card -->
    <div class="card mb-4">
        <div class="card-body">
            <div class="row align-items-center">
                <div class="col-md-4">
                    <div class="bg-light rounded p-4 text-center" style="height: 200px; display: flex; align-items: center; justify-content: center;">
                        <div>
                            <div class="bg-primary rounded-circle mx-auto mb-3" style="width: 60px; height: 60px; display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-image text-white"></i>
                            </div>
                            <div class="fw-bold">YOUR</div>
                            <div class="fw-bold">IMAGE</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-8">
                    <h3 class="h5 mb-2">{postData.title}</h3>
                    <p class="text-muted mb-3">{postData.description}</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Key Metrics -->
    <div class="mb-4">
        <h3 class="h5 mb-3">Key Metrics</h3>
        <div class="row g-3">
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="text-muted small mb-1">Engagement</div>
                        <div class="h4 mb-1">{postData.metrics.engagement.value.toLocaleString()}</div>
                        <div class="text-success small">+{postData.metrics.engagement.change}% from yesterday</div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="text-muted small mb-1">Reach</div>
                        <div class="h4 mb-1">{postData.metrics.reach.value.toLocaleString()}</div>
                        <div class="text-success small">+{postData.metrics.reach.change}% from yesterday</div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <div class="text-muted small mb-1">Impressions</div>
                        <div class="h4 mb-1">{postData.metrics.impressions.value.toLocaleString()}</div>
                        <div class="text-success small">+{postData.metrics.impressions.change}% from yesterday</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Performance Over Time -->
    <div class="mb-4">
        <div class="card">
            <div class="card-body">
                <h3 class="h5 mb-3">Performance Over Time</h3>
                
                <div class="row align-items-center mb-4">
                    <div class="col-md-6">
                        <div class="text-muted small mb-1">Engagement Rate</div>
                        <div class="h2 mb-1">{postData.engagementRate.value}%</div>
                        <div class="text-success small">Last 30 Days +{postData.engagementRate.change}%</div>
                    </div>
                </div>
                
                <div style="height: 300px; position: relative; width: 100%;">
                    <canvas bind:this={chartCanvas} style="width: 100% !important; height: 100% !important;"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Engagement by Channel -->
    <div class="mb-4">
        <div class="card">
            <div class="card-body">
                <h3 class="h5 mb-3">Engagement by Channel</h3>
                <p class="text-muted small mb-4">See which platforms are driving the most engagement for this post</p>
                
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <div style="height: 300px; position: relative;">
                            <canvas bind:this={pieChartCanvas}></canvas>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="ps-3">
                            {#each Object.entries(channelData) as [channel, percentage], index}
                                <div class="d-flex align-items-center justify-content-between py-2">
                                    <div class="d-flex align-items-center">
                                        <div class="rounded-circle me-2" style="width: 12px; height: 12px; background-color: {['#E1306C', '#1877F2', '#1DA1F2', '#0077B5', '#FF0050'][index]};"></div>
                                        <span class="small fw-medium">{channel}</span>
                                    </div>
                                    <span class="small text-muted fw-bold">{percentage}%</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Conversion Rate Breakdown -->
    <div class="mb-4">
        <div class="card">
            <div class="card-body">
                <h3 class="h5 mb-2">Conversion Rate</h3>
                <p class="text-muted small mb-4">% of social visitors who take a desired action (purchase, signup)</p>
                
                <div class="row align-items-center mb-4">
                    <div class="col-md-6">
                        <div class="text-muted small mb-1">Overall Conversion Rate</div>
                        <div class="h2 mb-1">3.2%</div>
                        <div class="text-success small">+0.8% from last month</div>
                    </div>
                </div>
                
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <div style="height: 300px; position: relative;">
                            <canvas bind:this={conversionChartCanvas}></canvas>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="ps-3">
                            {#each Object.entries(conversionData) as [action, percentage], index}
                                <div class="d-flex align-items-center justify-content-between py-2">
                                    <div class="d-flex align-items-center">
                                        <div class="rounded-circle me-2" style="width: 12px; height: 12px; background-color: {['#10B981', '#3B82F6', '#8B5CF6', '#F59E0B'][index]};"></div>
                                        <span class="small fw-medium">{action}</span>
                                    </div>
                                    <span class="small text-muted fw-bold">{percentage}%</span>
                                </div>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    
    <!-- Sentiment Detection -->
    <div class="mb-4">
        <div class="card">
            <div class="card-body">
                <h3 class="h5 mb-2">Sentiment Detection</h3>
                <p class="text-muted small mb-4">AI-powered analysis of audience reactions and emotions in comments and interactions</p>
                
                <div class="row align-items-center mb-4">
                    <div class="col-md-6">
                        <div class="text-muted small mb-1">Overall Sentiment Score</div>
                        <div class="h2 mb-1">7.8/10</div>
                        <div class="text-success small">Predominantly positive audience reaction</div>
                    </div>
                </div>
                
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <div style="height: 300px; position: relative;">
                            <canvas bind:this={sentimentChartCanvas}></canvas>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="ps-3">
                            {#each Object.entries(sentimentData) as [sentiment, percentage], index}
                                <div class="d-flex align-items-center justify-content-between py-2">
                                    <div class="d-flex align-items-center">
                                        <div class="rounded-circle me-2" style="width: 12px; height: 12px; background-color: {['#10B981', '#6B7280', '#EF4444'][index]};"></div>
                                        <span class="small fw-medium">{sentiment}</span>
                                    </div>
                                    <span class="small text-muted fw-bold">{percentage}%</span>
                                </div>
                            {/each}
                            
                            <!-- Key insights -->
                            <div class="mt-4 pt-3 border-top">
                                <h6 class="small fw-bold text-muted mb-2">KEY INSIGHTS</h6>
                                <div class="small text-muted mb-2">
                                    <i class="fas fa-heart text-success me-2"></i>
                                    High positive engagement from younger demographics
                                </div>
                                <div class="small text-muted mb-2">
                                    <i class="fas fa-lightbulb text-warning me-2"></i>
                                    Comments mention product quality and value
                                </div>
                                <div class="small text-muted">
                                    <i class="fas fa-trending-up text-info me-2"></i>
                                    Sentiment improved 15% from last post
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</div>