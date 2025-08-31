<script>
    // @ts-nocheck
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';


    // IF USING A REAL API, REPLACE THE MOCK DATA WITH API CALLS
    // API endpoint URLs (these should point to backend/server routes that fetch from GCS)
    const X_API_URL = "http://127.0.0.1:8000/api/x/"; // Should return tweets.json from GCS
    const IG_API_URL = "http://127.0.0.1:8000/api/instagram/"; // Should return instagram.json from GCS
    const FB_API_URL = "http://127.0.0.1:8000/api/facebook/"; // Should return facebook_post.json from GCS


    // State for fetched data
    let xData = null;
    let instagramData = null;
    let facebookData = null;


    // Fetch data from Google Cloud Storage (GCS)
    async function fetchGCSData() {
        console.log('Starting to fetch data from backend...');
        try {
            console.log('Fetching from URLs:', { X_API_URL, IG_API_URL, FB_API_URL });
            
            // Fetch X/Twitter data (this should work)
            try {
                const xRes = await fetch(X_API_URL);
                console.log('X API response status:', xRes.status);
                if (xRes.ok) {
                    xData = await xRes.json();
                    console.log('X data fetched successfully:', xData);
                } else {
                    console.warn('X API failed with status:', xRes.status);
                }
            } catch (err) {
                console.error('Error fetching X data:', err);
            }
            
            // Fetch Instagram data (may have permission issues)
            try {
                const igRes = await fetch(IG_API_URL);
                console.log('Instagram API response status:', igRes.status);
                if (igRes.ok) {
                    const igResult = await igRes.json();
                    // Check if it's an error response from Instagram API
                    if (igResult.error) {
                        console.warn('Instagram API returned error:', igResult.error);
                        instagramData = null;
                    } else {
                        instagramData = igResult;
                        console.log('Instagram data fetched successfully:', instagramData);
                    }
                } else {
                    console.warn('Instagram API failed with status:', igRes.status);
                }
            } catch (err) {
                console.error('Error fetching Instagram data:', err);
            }
            
            // Fetch Facebook data (may not exist in GCS)
            try {
                const fbRes = await fetch(FB_API_URL);
                console.log('Facebook API response status:', fbRes.status);
                if (fbRes.ok) {
                    facebookData = await fbRes.json();
                    console.log('Facebook data fetched successfully:', facebookData);
                } else {
                    console.warn('Facebook API failed with status:', fbRes.status);
                }
            } catch (err) {
                console.error('Error fetching Facebook data:', err);
            }
            
            console.log('Final data state:', { 
                hasXData: !!xData, 
                hasInstagramData: !!instagramData, 
                hasFacebookData: !!facebookData 
            });
            
        } catch (err) {
            console.error("Error fetching GCS data:", err);
        }
    }


    // Example of how to display fetched data (replace dummy data)
    // For X (Twitter) metrics
    $: xMetrics = xData
        ? {
            totalTweets: xData.data.length,
            totalLikes: xData.data.reduce((sum, t) => sum + t.public_metrics.like_count, 0),
            totalRetweets: xData.data.reduce((sum, t) => sum + t.public_metrics.retweet_count, 0),
            totalReplies: xData.data.reduce((sum, t) => sum + t.public_metrics.reply_count, 0),
            totalImpressions: xData.data.reduce((sum, t) => sum + (t.public_metrics.impression_count || 0), 0)
        }
        : {
            totalTweets: 0,
            totalLikes: 0,
            totalRetweets: 0,
            totalReplies: 0,
            totalImpressions: 0
        };

    // For Instagram metrics
    $: igMetrics = instagramData
        ? {
            totalPosts: instagramData.data.length,
            totalLikes: instagramData.data.reduce((sum, p) => sum + (p.like_count || 0), 0),
            totalComments: instagramData.data.reduce((sum, p) => sum + (p.comments_count || 0), 0)
        }
        : {
            totalPosts: 0,
            totalLikes: 0,
            totalComments: 0
        };

    // For Facebook metrics
    $: fbMetrics = facebookData
        ? {
            totalPosts: facebookData.data.length,
            totalLikes: facebookData.data.reduce((sum, p) => sum + (p.likes?.summary?.total_count || 0), 0),
            totalComments: facebookData.data.reduce((sum, p) => sum + (p.comments?.summary?.total_count || 0), 0)
        }
        : {
            totalPosts: 0,
            totalLikes: 0,
            totalComments: 0
        };
    

    // Engagement, Reach, New Followers for each platform
    $: instagramEngagement = instagramData
        ? instagramData.data.reduce((sum, post) => sum + (post.like_count || 0) + (post.comments_count || 0), 0)
        : 0;

    $: instagramReach = instagramData
        ? instagramData.data.reduce((sum, post) => sum + (post.reach || 0), 0) // If reach is available per post
        : 0;

    $: instagramNewFollowers = instagramData
        ? (instagramData.new_followers || 0)
        : 0;

    // X (Twitter)
    $: xEngagement = xData
        ? xData.data.reduce((sum, tweet) => sum + tweet.public_metrics.like_count + tweet.public_metrics.retweet_count + tweet.public_metrics.reply_count, 0)
        : 0;

    $: xReach = xData
        ? xData.data.reduce((sum, tweet) => sum + (tweet.public_metrics.impression_count || 0), 0)
        : 0;

    $: xNewFollowers = xData
        ? (xData.new_followers || 0)
        : 0;

    // Facebook
    $: fbEngagement = facebookData
        ? facebookData.data.reduce((sum, post) => sum + (post.likes?.summary?.total_count || 0) + (post.comments?.summary?.total_count || 0), 0)
        : 0;

    $: fbReach = facebookData
        ? (facebookData.insights?.page_impressions || 0)
        : 0;

    $: fbNewFollowers = facebookData
        ? (facebookData.insights?.page_fans || 0)
        : 0;

    // Total across all platforms
    $: totalEngagement = instagramEngagement + xEngagement + fbEngagement;
    $: totalReach = instagramReach + xReach + fbReach;
    $: totalNewFollowers = instagramNewFollowers + xNewFollowers + fbNewFollowers;
    
    // Calculate overall engagement rate from all platforms
    $: overallEngagementRate = totalReach > 0 ? ((totalEngagement / totalReach) * 100) : 0;
    
    // Format engagement rate for display
    $: formattedEngagementRate = overallEngagementRate.toFixed(1);
    
    // Format reach for display
    $: formattedReach = totalReach > 1000 ? `${(totalReach/1000).toFixed(1)}K` : totalReach.toLocaleString();
    

    let selectedRange = "Last 30 days";
    let ranges = ["Last 7 days", "Last 30 days", "Last 90 days"];


    // Social media platform tracking
    let selectedPlatform = "All Platforms";

    let platforms = [
        "All Platforms",
        "Instagram", 
        "Facebook", 
        "TikTok", 
        "X",
        "LinkedIn", 
    ];  

    
    // Post selection
    let selectedPost = "All Posts";

    // Helper function to truncate text for display
    function truncateText(text, maxLength = 50) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        // Try to break at word boundary if possible
        const truncated = text.substring(0, maxLength);
        const lastSpaceIndex = truncated.lastIndexOf(' ');
        if (lastSpaceIndex > maxLength * 0.7) { // Only break at word if it's not too short
            return truncated.substring(0, lastSpaceIndex) + '...';
        }
        return truncated + '...';
    }

    // Store mapping of truncated text to original text for reference
    let postTextMapping = {};

    // Dynamically filter posts based on selectedPlatform and loaded API data
    $: posts = (() => {
        postTextMapping = {}; // Reset mapping
        
        let rawPosts = [];
        if (selectedPlatform === "All Platforms") {
            rawPosts = [
                ...(xData?.data || []),
                ...(instagramData?.data || []),
                ...(facebookData?.data || [])
            ].map(post => post.text || post.caption || post.message).filter(Boolean);
        } else if (selectedPlatform === "Instagram") {
            rawPosts = (instagramData?.data || []).map(post => post.caption).filter(Boolean);
        } else if (selectedPlatform === "Facebook") {
            rawPosts = (facebookData?.data || []).map(post => post.message).filter(Boolean);
        } else if (selectedPlatform === "X") {
            rawPosts = (xData?.data || []).map(post => post.text).filter(Boolean);
        }
        
        // Create truncated versions and maintain mapping
        return rawPosts.map(originalText => {
            const truncatedText = truncateText(originalText);
            postTextMapping[truncatedText] = originalText;
            return truncatedText;
        });
    })();
    

    // Platform-specific data multipliers for different growth rates
    // TODO: FETCH FROM API - Replace with real-time platform analytics data
    let platformMultipliers = {
        "All Platforms": { likes: 1.0, comments: 1.0, shares: 1.0 },
        "Instagram": { likes: 1.8, comments: 0.9, shares: 0.5 }, // High likes, fewer shares
        "Facebook": { likes: 1.2, comments: 1.4, shares: 1.3 }, // Balanced, good sharing
        "LinkedIn": { likes: 0.6, comments: 1.1, shares: 0.9 }, // Professional, thoughtful engagement
        "TikTok": { likes: 2.5, comments: 1.8, shares: 0.3 }, // Viral likes & comments, low shares
        "X": { likes: 1.0, comments: 1.6, shares: 2.2 }, // High conversation & sharing
    };
    

    // Post-specific data multipliers for different performance
    // TODO: FETCH FROM API - Replace with real post performance metrics
    let postMultipliers = {
        "All Posts": { likes: 1.0, comments: 1.0, shares: 1.0 },
        "Summer Campaign Launch": { likes: 2.2, comments: 1.8, shares: 2.5 }, // High performing campaign
        "Product Feature Update": { likes: 1.4, comments: 2.1, shares: 1.6 }, // Good engagement, lots of questions
        "Behind the Scenes Video": { likes: 1.9, comments: 1.5, shares: 1.2 }, // High likes, moderate sharing
        "Customer Success Story": { likes: 1.3, comments: 1.7, shares: 2.0 }, // Inspiring, gets shared
        "Weekly Tips & Tricks": { likes: 1.1, comments: 1.3, shares: 1.4 }, // Steady, useful content
        "Brand Partnership Announcement": { likes: 1.6, comments: 0.8, shares: 1.8 }, // Good reach, fewer comments
        "User Generated Content": { likes: 2.0, comments: 1.9, shares: 1.7 }, // Community loves it
        "Flash Sale Promotion": { likes: 1.5, comments: 0.9, shares: 2.3 } // High shares, fewer comments
    };

    
    // Chart.js variables
    let chartCanvas;
    let chart = null;
    let engagementChartCanvas;
    let engagementChart = null;
    let labels = [];
    let likes = [];
    let comments = [];
    let shares = [];
    let totalLikes = 0;
    let totalComments = 0;
    let totalShares = 0;
    let t = 0;
    let chartInterval = null;


    // Tab state for Engagement/Reach
    let activeTab = "Engagement";


    // Helper: Get current engagement and reach data from all platforms
    function getCurrentData() {
        // Since timeline data isn't available, return current accumulated values
        // This will be used for the Performance Over Time chart
        
        if (!instagramData && !xData && !facebookData) {
            return { 
                currentEngagementRate: 0,
                currentReach: 0,
                hasData: false
            };
        }
        
        return {
            currentEngagementRate: overallEngagementRate,
            currentReach: totalReach,
            hasData: true
        };
    }


    onMount(() => {
        // Use dummy data for now
        // When ready, call fetchGCSData() to use real data
        fetchGCSData();

        // Initialize with zero starting values like the original
        totalLikes = 0;
        totalComments = 0;
        totalShares = 0;
        t = 0;
        labels = [];
        likes = [];
        comments = [];
        shares = [];
        
        // Wait a bit for Chart.js to load, then initialize
        setTimeout(() => {
            initChart();
            initEngagementChart();
        }, 100);
    });


    // Live Social Media Analytics
    function initChart() {
        if (chartCanvas && typeof Chart !== 'undefined') {
            const ctx = chartCanvas.getContext('2d');

            // --- Real API data fetching (commented out for now) ---
            // const timeline = getTimelineData();
            // const labels = timeline.labels;
            // const likes = timeline.likes;
            // const comments = timeline.comments;
            // const shares = timeline.shares;

            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels, // dummy/simulated data for now
                    datasets: [
                        {
                            label: 'Likes',
                            data: likes,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            fill: true,
                            tension: 0.3,
                            borderWidth: 3,
                            pointRadius: 4,
                            pointBackgroundColor: 'white',
                            pointBorderColor: 'rgba(54, 162, 235, 1)'
                        },
                        {
                            label: 'Comments',
                            data: comments,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            fill: true,
                            tension: 0.3,
                            borderWidth: 3,
                            pointRadius: 4,
                            pointBackgroundColor: 'white',
                            pointBorderColor: 'rgba(75, 192, 192, 1)'
                        },
                        {
                            label: 'Shares',
                            data: shares,
                            borderColor: 'rgba(255, 159, 64, 1)',
                            backgroundColor: 'rgba(255, 159, 64, 0.2)',
                            fill: true,
                            tension: 0.3,
                            borderWidth: 3,
                            pointRadius: 4,
                            pointBackgroundColor: 'white',
                            pointBorderColor: 'rgba(255, 159, 64, 1)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    animation: false,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                font: { size: 14 },
                                color: '#333'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.7)',
                            titleFont: { size: 14 },
                            bodyFont: { size: 13 },
                            padding: 10,
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: 'Time', color: '#666', font: { size: 14 } },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: { 
                                color: '#666',
                                callback: function(value, index, values) {
                                    // Get the actual label value from the labels array
                                    const labelValue = this.chart.data.labels[index];
                                    if (labelValue !== undefined) {
                                        const hours = labelValue % 24;
                                        return `${hours.toString().padStart(2, '0')}:00`;
                                    }
                                    return '';
                                }
                            }
                        },
                        y: {
                            title: { display: true, text: 'Count', color: '#666', font: { size: 14 } },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: { color: '#666' },
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                font: { size: 14 },
                                color: '#333'
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0,0,0,0.7)',
                            titleFont: { size: 14 },
                            bodyFont: { size: 13 },
                            padding: 10,
                            cornerRadius: 8
                        },
                        annotation: {
                            annotations: {
                                dayLine: {
                                    type: 'line',
                                    xMin: 0,
                                    xMax: 0,
                                    borderColor: 'rgba(255, 0, 0, 0.5)',
                                    borderWidth: 2,
                                    borderDash: [5, 5],
                                    label: {
                                        content: 'Day Boundary',
                                        enabled: true,
                                        position: 'start'
                                    }
                                }
                            }
                        }
                    }
                }
            });

            // Start the real-time data simulation immediately
            startDataSimulation();
        } else {
            // If Chart.js isn't loaded yet, try again after a delay
            setTimeout(initChart, 100);
        }
    }


    // Performance Over Time Chart
    function initEngagementChart() {
        if (engagementChartCanvas && typeof Chart !== 'undefined') {
            const ctx = engagementChartCanvas.getContext('2d');

            // Use dummy data aligned with KPI cards
            let labels = [];
            let data = [];
            
            if (activeTab === "Engagement") {
                // Dummy engagement rate data building up to 6.6% (matching KPI card)
                data = [4.2, 5.1, 4.8, 5.9, 6.6];
                labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'];
            } else {
                // Dummy reach data building up to 125.3K (matching KPI card)
                data = [87.7, 100.3, 112.8, 119.5, 125.3];
                labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'];
            }

            engagementChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        data: data,
                        borderColor: '#4f46e5',
                        backgroundColor: 'rgba(79, 70, 229, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointRadius: 4,
                        pointHoverRadius: 6,
                        pointBackgroundColor: 'white',
                        pointBorderColor: '#4f46e5',
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
                            borderColor: '#4f46e5',
                            borderWidth: 1,
                            cornerRadius: 8,
                            displayColors: false,
                            callbacks: {
                                label: function(context) {
                                    if (activeTab === "Engagement") {
                                        return `Engagement Rate: ${context.parsed.y.toFixed(1)}%`;
                                    } else {
                                        return `Reach: ${context.parsed.y.toFixed(1)}K`;
                                    }
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
            setTimeout(initEngagementChart, 100);
        }
    }


    // Function to handle tab changes
    function switchTab(tabName) {
        activeTab = tabName;
        if (engagementChart) {
            updateChartData();
        }
    }
    

    // Function to update chart data based on active tab
    function updateChartData() {
        if (!engagementChart) return;

        // Use dummy data aligned with KPI cards
        let data;
        
        if (activeTab === "Engagement") {
            // Dummy engagement rate data building up to 6.6% (matching KPI card)
            data = [4.2, 5.1, 4.8, 5.9, 6.6];
        } else {
            // Dummy reach data building up to 125.3K (matching KPI card)
            data = [87.7, 100.3, 112.8, 119.5, 125.3];
        }
        
        // Update labels to match
        engagementChart.data.labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current'];
        engagementChart.data.datasets[0].data = data;
        engagementChart.update();
    }


    function startDataSimulation() {
        if (chartInterval) {
            clearInterval(chartInterval);
        }
        
        // TODO: REPLACE WITH REAL-TIME API CALLS - This entire simulation should be replaced with WebSocket or periodic API calls
        chartInterval = setInterval(() => {
            const platformMultiplier = platformMultipliers[selectedPlatform];
            const postMultiplier = postMultipliers[selectedPost];
            
            // TODO: FETCH FROM API - Get real-time engagement data instead of simulation
            // Apply both platform and post-specific growth rates
            const combinedLikesMultiplier = platformMultiplier.likes * postMultiplier.likes;
            const combinedCommentsMultiplier = platformMultiplier.comments * postMultiplier.comments;
            const combinedSharesMultiplier = platformMultiplier.shares * postMultiplier.shares;
            
            const likesIncrease = Math.floor(Math.random() * 10) * combinedLikesMultiplier;
            const commentsIncrease = Math.floor(Math.random() * 5) * combinedCommentsMultiplier;
            const sharesIncrease = Math.floor(Math.random() * 3) * combinedSharesMultiplier;
            
            // Add random spikes for all engagement types
            let finalLikesIncrease = likesIncrease;
            let finalCommentsIncrease = commentsIncrease;
            let finalSharesIncrease = sharesIncrease;
            
            // Likes spikes (10% chance)
            if (Math.random() < 0.1) {
                const spikeMultiplier = 3 + Math.random() * 5;
                finalLikesIncrease = likesIncrease * spikeMultiplier;
            }
            
            // Comments spikes (8% chance, slightly less frequent)
            if (Math.random() < 0.08) {
                const spikeMultiplier = 2.5 + Math.random() * 4;
                finalCommentsIncrease = commentsIncrease * spikeMultiplier;
            }
            
            // Shares spikes (6% chance, least frequent but can be very viral)
            if (Math.random() < 0.06) {
                const spikeMultiplier = 4 + Math.random() * 6;
                finalSharesIncrease = sharesIncrease * spikeMultiplier;
            }
            
            totalLikes += finalLikesIncrease;
            totalComments += finalCommentsIncrease;
            totalShares += finalSharesIncrease;

            // Cycle time from 0-23, but keep data continuous
            const displayTime = t % 24;

            labels.push(displayTime);
            likes.push(totalLikes);
            comments.push(totalComments);
            shares.push(totalShares);
            
            t += 1;

            // Keep only 24 hours of data (one day)
            if (labels.length > 24) {
                labels.shift();
                likes.shift();
                comments.shift();
                shares.shift();
            }

            if (chart) {
                chart.update();
            }
        }, 5000);
    }


    // Function to reset chart data when platform changes
    function resetChartData() {
        labels = [];
        likes = [];
        comments = [];
        shares = [];
        totalLikes = 0;
        totalComments = 0;
        totalShares = 0;
        t = 0;
        
        if (chart) {
            chart.update();
        }
    }
    

    // Function to handle platform changes
    function handlePlatformChange(event) {
        const newPlatform = event.target.value;
        selectedPlatform = newPlatform;
            // posts will update automatically due to reactive statement above
            // No need to restart data simulation, just let current cycle apply new multipliers
    }


    function handlePostChange(event) {
        const newPost = event.target.value;
        selectedPost = newPost;
        // No need to restart data simulation, just let current cycle apply new multipliers
    }


    // Function to handle post clicks and redirect to library/PublishedPost
    function handlePostClick() {
        goto('/library/PublishedPost');
    }


    onDestroy(() => {
        if (chartInterval) {
            clearInterval(chartInterval);
        }
        if (chart) {
            chart.destroy();
        }
        if (engagementChart) {
            engagementChart.destroy();
        }
    });
</script>

<div class="container py-4 mt-4" style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); min-height: 100vh;">
    <div class="mb-4 text-center">
        <h1 class="mb-2" style="font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 2.5rem;">
            <i class="fas fa-chart-line me-3" style="color: #667eea;"></i>Analytics Overview
        </h1>
        <div class="text-muted mb-4" style="font-size:1.1rem; color: #718096 !important; font-weight: 500;">
            Analyze your social media performance across all connected accounts.
        </div>
    </div>

    <div class="mb-4 d-flex justify-content-center">
        <select class="form-select" style="width: auto; border-radius: 15px; border: 2px solid #e2e8f0; padding: 10px 20px; font-weight: 600; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.05);" bind:value={selectedRange}>
            {#each ranges as range}
                <option value={range}>{range}</option>
            {/each}
        </select>
    </div>

    <div class="row mb-4 g-3">
        <div class="col-md-3">
            <div class="card text-center border-0 shadow-sm h-100" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <div class="card-body d-flex flex-column justify-content-center">
                    <div class="mb-2">
                        <i class="fas fa-eye" style="font-size: 2rem; opacity: 0.8;"></i>
                    </div>
                    <!-- Dummy Total Reach -->
                    <div class="fw-bold" style="font-size:1.8rem;">125,340</div>
                    <div style="opacity: 0.9; font-weight: 500;">Total Reach</div>
                    <div class="mt-2 px-2 py-1 rounded" style="background: rgba(255,255,255,0.2); font-size:0.9rem; display: inline-block;">
                        <i class="fas fa-arrow-up me-1"></i>+12%
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center border-0 shadow-sm h-100" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                <div class="card-body d-flex flex-column justify-content-center">
                    <div class="mb-2">
                        <i class="fas fa-heart" style="font-size: 2rem; opacity: 0.8;"></i>
                    </div>
                    <!-- Dummy Total Engagement -->
                    <div class="fw-bold" style="font-size:1.8rem;">8,234</div>
                    <div style="opacity: 0.9; font-weight: 500;">Engagement</div>
                    <div class="mt-2 px-2 py-1 rounded" style="background: rgba(255,255,255,0.2); font-size:0.9rem; display: inline-block;">
                        <i class="fas fa-arrow-up me-1"></i>+8%
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center border-0 shadow-sm h-100" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
                <div class="card-body d-flex flex-column justify-content-center">
                    <div class="mb-2">
                        <i class="fas fa-chart-line" style="font-size: 2rem; opacity: 0.8;"></i>
                    </div>
                    <!-- Dummy Engagement Rate -->
                    <div class="fw-bold" style="font-size:1.8rem;">6.6%</div>
                    <div style="opacity: 0.9; font-weight: 500;">Engagement Rate</div>
                    <div class="mt-2 px-2 py-1 rounded" style="background: rgba(255,255,255,0.2); font-size:0.9rem; display: inline-block;">
                        <i class="fas fa-arrow-up me-1"></i>+2%
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center border-0 shadow-sm h-100" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white;">
                <div class="card-body d-flex flex-column justify-content-center">
                    <div class="mb-2">
                        <i class="fas fa-user-plus" style="font-size: 2rem; opacity: 0.8;"></i>
                    </div>
                    <!-- Dummy New Followers -->
                    <div class="fw-bold" style="font-size:1.8rem;">1,247</div>
                    <div style="opacity: 0.9; font-weight: 500;">New Followers</div>
                    <div class="mt-2 px-2 py-1 rounded" style="background: rgba(255,255,255,0.2); font-size:0.9rem; display: inline-block;">
                        <i class="fas fa-arrow-up me-1"></i>+15%
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabs for Engagement/Reach -->
    <div class="d-flex mb-3" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 6px; width: 100%; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
        <button 
            class="btn flex-fill" 
            type="button" 
            style="background-color: {activeTab === 'Engagement' ? 'white' : 'transparent'}; border: none; border-radius: 12px; font-weight: 600; padding: 12px 20px; margin: 0; transition: all 0.3s ease; {activeTab === 'Engagement' ? 'box-shadow: 0 2px 8px rgba(0,0,0,0.15); transform: translateY(-1px);' : ''} color: {activeTab === 'Engagement' ? '#667eea' : 'rgba(255,255,255,0.8)'};"
            on:click={() => switchTab('Engagement')}
        >
            <i class="fas fa-heart me-2"></i>
            Engagement
        </button>
        <button 
            class="btn flex-fill" 
            type="button" 
            style="background-color: {activeTab === 'Reach' ? 'white' : 'transparent'}; border: none; border-radius: 12px; font-weight: 600; padding: 12px 20px; margin: 0; transition: all 0.3s ease; {activeTab === 'Reach' ? 'box-shadow: 0 2px 8px rgba(0,0,0,0.15); transform: translateY(-1px);' : ''} color: {activeTab === 'Reach' ? '#667eea' : 'rgba(255,255,255,0.8)'};"
            on:click={() => switchTab('Reach')}
        >
            <i class="fas fa-eye me-2"></i>
            Reach
        </button>
    </div>

    <!-- Engagement Over Time Chart -->
    <div class="mb-4">
        <div class="card border-0 shadow-lg" style="background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%); border-radius: 20px;">
            <div class="card-body" style="padding: 2rem;">
                <div class="d-flex align-items-center mb-3">
                    <div class="rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        <i class="fas fa-chart-area text-white" style="font-size: 1.2rem;"></i>
                    </div>
                    <div>
                        <h5 class="card-title mb-1" style="color: #2d3748; font-weight: 700;">Performance Over Time</h5>
                        <p class="text-muted small mb-0" style="color: #718096 !important;">{activeTab} {activeTab === 'Engagement' ? 'Rate' : ''}</p>
                    </div>
                </div>
                
                <div class="row align-items-center mb-4">
                    <div class="col-md-6">
                        {#if activeTab === 'Engagement'}
                            <!-- Dummy engagement rate data aligned with KPI cards -->
                            <div class="fw-bold" style="font-size:2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                                6.6%
                            </div>
                            <div class="text-muted">Current Engagement Rate
                                <span class="badge rounded-pill" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 4px 8px;">
                                    <i class="fas fa-chart-line me-1"></i>Demo Data
                                </span>
                            </div>
                        {:else}
                            <!-- Dummy reach data aligned with KPI cards -->
                            <div class="fw-bold" style="font-size:2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                                125.3K
                            </div>
                            <div class="text-muted">Current Total Reach
                                <span class="badge rounded-pill" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 4px 8px;">
                                    <i class="fas fa-chart-line me-1"></i>Demo Data
                                </span>
                            </div>
                        {/if}
                    </div>
                </div>
                
                <div style="height: 300px; position: relative; width: 100%; background: white; border-radius: 15px; padding: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
                    <canvas bind:this={engagementChartCanvas} style="width: 100% !important; height: 100% !important;"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Top Platforms Table -->
    <div class="mb-4">
        <div class="d-flex align-items-center mb-3">
            <div class="rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 45px; height: 45px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <i class="fas fa-share-alt text-white" style="font-size: 1.1rem;"></i>
            </div>
            <div class="fw-bold" style="font-size: 1.3rem; color: #2d3748;">Top Platforms</div>
        </div>
        <div class="card border-0 shadow-lg" style="border-radius: 20px; overflow: hidden;">
            <div class="card-body px-0 py-0">
                <table class="table mb-0" style="border-radius: 20px; overflow: hidden;">
                    <thead style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <tr>
                            <th style="border: none; padding: 1rem 2rem; font-weight: 600;">Platform</th>
                            <th style="border: none; padding: 1rem 1rem; font-weight: 600;">Engagement</th>
                            <th style="border: none; padding: 1rem 2rem; font-weight: 600;">Reach</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="cursor: pointer; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#f8f9ff'" onmouseout="this.style.backgroundColor='white'">
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0;">
                                <span class="rounded-circle d-inline-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; background:linear-gradient(135deg,#fdc468 0%,#df4996 50%,#4f5bd5 100%); box-shadow: 0 4px 12px rgba(253, 196, 104, 0.4);">
                                    <i class="fab fa-instagram" style="color:white; font-size: 1.2rem;"></i>
                                </span>
                                <span style="font-weight: 600; color: #2d3748;">Instagram</span>
                            </td>
                            <td style="padding: 1rem 1rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">1,234</td>
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">2,345</td>
                        </tr>
                        <tr style="cursor: pointer; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#f8f9ff'" onmouseout="this.style.backgroundColor='white'">
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0;">
                                <span class="rounded-circle d-inline-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; background:#1877F3; box-shadow: 0 4px 12px rgba(24, 119, 243, 0.4);">
                                    <i class="fab fa-facebook" style="color:white; font-size: 1.2rem;"></i>
                                </span>
                                <span style="font-weight: 600; color: #2d3748;">Facebook</span>
                            </td>
                            <td style="padding: 1rem 1rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">1,122</td>
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">2,233</td>
                        </tr>
                        <tr style="cursor: pointer; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#f8f9ff'" onmouseout="this.style.backgroundColor='white'">
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0;">
                                <span class="rounded-circle d-inline-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; background:#000000; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);">
                                    <i class="fab fa-x-twitter" style="color:white; font-size: 1.2rem;"></i>
                                </span>
                                <span style="font-weight: 600; color: #2d3748;">X</span>
                            </td>
                            <td style="padding: 1rem 1rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">1,010</td>
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">2,121</td>      
                        </tr>
                        <tr style="cursor: pointer; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#f8f9ff'" onmouseout="this.style.backgroundColor='white'">
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0;">
                                <span class="rounded-circle d-inline-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; background:#0a66c2; box-shadow: 0 4px 12px rgba(10, 102, 194, 0.4);">
                                    <i class="fab fa-linkedin" style="color:white; font-size: 1.2rem;"></i>
                                </span>
                                <span style="font-weight: 600; color: #2d3748;">LinkedIn</span>
                            </td>
                            <td style="padding: 1rem 1rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">800</td>
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0; font-weight: 600; color: #4a5568;">2,010</td>
                        </tr>
                        <tr style="cursor: pointer; transition: all 0.3s ease;" onmouseover="this.style.backgroundColor='#f8f9ff'" onmouseout="this.style.backgroundColor='white'">
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0; border-bottom: none;">
                                <span class="rounded-circle d-inline-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; background:#000000; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
                                    <i class="fab fa-tiktok" style="color:white; font-size: 1.2rem;"></i>
                                </span>
                                <span style="font-weight: 600; color: #2d3748;">TikTok</span>
                            </td>
                            <td style="padding: 1rem 1rem; border-color: #e2e8f0; border-bottom: none; font-weight: 600; color: #4a5568;">800</td>
                            <td style="padding: 1rem 2rem; border-color: #e2e8f0; border-bottom: none; font-weight: 600; color: #4a5568;">1,900</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Live Social Media Analytics Dashboard -->
    <div class="card border-0 shadow-lg mt-5" style="border-radius: 20px; background: linear-gradient(135deg, #fafbff 0%, #f0f4ff 100%);">
        <div class="card-body" style="padding: 2rem;">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <div class="d-flex align-items-center">
                    <div class="rounded-circle me-3 d-flex align-items-center justify-content-center" style="width: 50px; height: 50px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                        <i class="fas fa-broadcast-tower text-white" style="font-size: 1.2rem;"></i>
                    </div>
                    <div>
                        <h5 class="card-title mb-0" style="color: #2d3748; font-weight: 700;">Live Social Media Analytics</h5>
                        <p class="text-muted mb-0" style="font-size: 0.9rem;">Real-time engagement tracking</p>
                    </div>
                </div>
                <div class="d-flex align-items-center gap-3">
                    <div class="d-flex align-items-center">
                        <label for="platformSelect" class="form-label me-2 mb-0" style="font-size:0.9rem; font-weight: 600; color: #4a5568;">Platform:</label>
                        <select id="platformSelect" class="form-select form-select-sm" style="width:auto; border-radius: 10px; border: 2px solid #e2e8f0; font-weight: 500;" bind:value={selectedPlatform} on:change={handlePlatformChange}>
                            {#each platforms as platform}
                                <option value={platform}>{platform}</option>
                            {/each}
                        </select>
                    </div>
                    <div class="d-flex align-items-center">
                        <label for="postSelect" class="form-label me-2 mb-0" style="font-size:0.9rem; font-weight: 600; color: #4a5568;">Post:</label>
                        <select id="postSelect" class="form-select form-select-sm post-select" style="max-width: 300px; border-radius: 10px; border: 2px solid #e2e8f0; font-weight: 500;" bind:value={selectedPost} on:change={handlePostChange}>
                            <option value="All Posts">All Posts</option>
                            {#each posts as post}
                                <option value={post} title={post}>{post}</option>
                            {/each}
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="mb-4">
                <span class="badge me-2" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 500;">
                    <i class="fas fa-broadcast-tower me-2"></i>{selectedPlatform}
                </span>
                <span class="badge" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 8px 16px; border-radius: 20px; font-weight: 500;">
                    <i class="fas fa-file-alt me-2"></i>{selectedPost}
                </span>
            </div>
        
            <div style="background: white; border-radius: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); padding: 25px; border: 1px solid rgba(102, 126, 234, 0.1);">
                <canvas bind:this={chartCanvas} width="800" height="400"></canvas>
            </div>
            <div class="text-muted mt-3 d-flex align-items-center" style="font-size:0.95rem;">
                <div class="rounded-circle me-2 d-flex align-items-center justify-content-center" style="width: 8px; height: 8px; background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);"></div>
                Real-time analytics showing likes, comments, and shares. Data updates every hour.
            </div>
        </div>
    </div>
</div>

<style>
    /* Post selection dropdown styling */
    .post-select {
        min-width: 200px;
        max-width: 300px;
    }
    
    .post-select option {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 300px;
    }
    
    /* Ensure dropdowns don't break layout on mobile */
    @media (max-width: 768px) {
        .post-select {
            max-width: 250px;
            min-width: 150px;
        }
    }
    
    @media (max-width: 576px) {
        .post-select {
            max-width: 200px;
            min-width: 120px;
        }
    }
</style>
