<script>
    // @ts-nocheck
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    
    let selectedRange = "Last 30 days";
    let ranges = ["Last 7 days", "Last 30 days", "Last 90 days"];
    
    // Post selection
    let selectedPost = "All Posts";
    let posts = [
        "All Posts",
        "Summer Campaign Launch",
        "Product Feature Update",
        "Behind the Scenes Video",
        "Customer Success Story",
        "Weekly Tips & Tricks",
        "Brand Partnership Announcement",
        "User Generated Content",
        "Flash Sale Promotion"
    ]; // Mock data --> should be fetched from backend in real app
    
    // Social media platform tracking
    let selectedPlatform = "All Platforms";
    let platforms = [
        "All Platforms",
        "Instagram", 
        "Facebook", 
        "TikTok", 
        "Twitter/X",
        "LinkedIn", 
    ];
    
    // Platform-specific data multipliers for different growth rates
    let platformMultipliers = {
        "All Platforms": { likes: 1.0, comments: 1.0, shares: 1.0 },
        "Instagram": { likes: 1.8, comments: 0.9, shares: 0.5 }, // High likes, fewer shares
        "Facebook": { likes: 1.2, comments: 1.4, shares: 1.3 }, // Balanced, good sharing
        "LinkedIn": { likes: 0.6, comments: 1.1, shares: 0.9 }, // Professional, thoughtful engagement
        "TikTok": { likes: 2.5, comments: 1.8, shares: 0.3 }, // Viral likes & comments, low shares
        "Twitter/X": { likes: 1.0, comments: 1.6, shares: 2.2 }, // High conversation & sharing
    };
    
    // Post-specific data multipliers for different performance
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

    onMount(() => {
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

    function initChart() {
        if (chartCanvas && typeof Chart !== 'undefined') {
            const ctx = chartCanvas.getContext('2d');
            
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
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

    function initEngagementChart() {
        if (engagementChartCanvas && typeof Chart !== 'undefined') {
            const ctx = engagementChartCanvas.getContext('2d');
            
            // Sample engagement rate data over time - showing positive growth trend
            const data = [0.8, 1.2, 1.0, 1.4, 1.7, 1.5, 1.9, 2.1, 2.0, 2.3, 2.4, 2.5];
            const labels = ['4W Ago', '', '', '3W Ago', '', '', '2W Ago', '', '', '1W Ago', '', 'Now'];
            
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
        
        let data, chartTitle, chartValue, chartChange, chartChangeClass;
        
        if (activeTab === "Engagement") {
            // Engagement data - showing positive growth trend
            data = [0.8, 1.2, 1.0, 1.4, 1.7, 1.5, 1.9, 2.1, 2.0, 2.3, 2.4, 2.5];
            chartTitle = "Engagement Rate";
            chartValue = "2.5%";
            chartChange = "+2%";
            chartChangeClass = "text-success";
        } else {
            // Reach data - showing different trend
            data = [8.2, 9.1, 8.8, 10.2, 11.5, 10.8, 12.1, 13.2, 12.8, 14.1, 13.7, 12.5];
            chartTitle = "Reach Rate";
            chartValue = "12.5K";
            chartChange = "+15%";
            chartChangeClass = "text-success";
        }
        
        engagementChart.data.datasets[0].data = data;
        engagementChart.update();
    }

    function startDataSimulation() {
        if (chartInterval) {
            clearInterval(chartInterval);
        }
        
        chartInterval = setInterval(() => {
            const platformMultiplier = platformMultipliers[selectedPlatform];
            const postMultiplier = postMultipliers[selectedPost];
            
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

<div class="container py-4">
    <h1 class="mb-2">Analytics Overview</h1>
    <div class="text-muted mb-4" style="font-size:1.05rem;">
        Analyze your social media performance across all connected accounts.
    </div>

    <div class="mb-3">
        <select class="form-select w-auto" bind:value={selectedRange}>
            {#each ranges as range}
                <option value={range}>{range}</option>
            {/each}
        </select>
    </div>

    <div class="row mb-4 g-3">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <div class="fw-bold" style="font-size:1.5rem;">12,345</div>
                    <div class="text-muted">Total Reach</div>
                    <div class="text-success mt-1" style="font-size:0.95rem;">+10%</div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <div class="fw-bold" style="font-size:1.5rem;">6,789</div>
                    <div class="text-muted">Engagement</div>
                    <div class="text-danger mt-1" style="font-size:0.95rem;">-5%</div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <div class="fw-bold" style="font-size:1.5rem;">5.5%</div>
                    <div class="text-muted">Engagement Rate</div>
                    <div class="text-success mt-1" style="font-size:0.95rem;">+2%</div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <div class="fw-bold" style="font-size:1.5rem;">456</div>
                    <div class="text-muted">New Followers</div>
                    <div class="text-success mt-1" style="font-size:0.95rem;">+8%</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Tabs for Engagement/Reach -->
    <div class="d-flex mb-3" style="background-color: #f8f9fa; border-radius: 12px; padding: 4px; width: 100%;">
        <button 
            class="btn flex-fill" 
            type="button" 
            style="background-color: {activeTab === 'Engagement' ? 'white' : 'transparent'}; border: none; border-radius: 8px; font-weight: 500; padding: 8px 16px; margin: 0; {activeTab === 'Engagement' ? 'box-shadow: 0 1px 3px rgba(0,0,0,0.1);' : ''} color: {activeTab === 'Engagement' ? '#000' : '#6c757d'};"
            on:click={() => switchTab('Engagement')}
        >
            Engagement
        </button>
        <button 
            class="btn flex-fill" 
            type="button" 
            style="background-color: {activeTab === 'Reach' ? 'white' : 'transparent'}; border: none; border-radius: 8px; font-weight: 500; padding: 8px 16px; margin: 0; {activeTab === 'Reach' ? 'box-shadow: 0 1px 3px rgba(0,0,0,0.1);' : ''} color: {activeTab === 'Reach' ? '#000' : '#6c757d'};"
            on:click={() => switchTab('Reach')}
        >
            Reach
        </button>
    </div>

    <!-- Engagement Over Time Chart -->
    <div class="mb-4">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title mb-1">Performance Over Time</h5>
                <p class="text-muted small mb-3">{activeTab} {activeTab === 'Engagement' ? 'Rate' : ''}</p>
                
                <div class="row align-items-center mb-4">
                    <div class="col-md-6">
                        {#if activeTab === 'Engagement'}
                            <div class="fw-bold" style="font-size:2rem;">2.5%</div>
                            <div class="text-muted">Last 30 Days <span class="text-success">+2%</span></div>
                        {:else}
                            <div class="fw-bold" style="font-size:2rem;">12.5K</div>
                            <div class="text-muted">Last 30 Days <span class="text-success">+15%</span></div>
                        {/if}
                    </div>
                </div>
                
                <div style="height: 300px; position: relative; width: 100%;">
                    <canvas bind:this={engagementChartCanvas} style="width: 100% !important; height: 100% !important;"></canvas>
                </div>
            </div>
        </div>
    </div>

    <!-- Top Platforms Table -->
    <div class="mb-4">
        <div class="fw-bold mb-2">Top Platforms</div>
        <div class="card">
            <div class="card-body px-4 py-2">
                <table class="table mb-0">
                    <thead>
                        <tr>
                            <th>Platform</th>
                            <th>Engagement</th>
                            <th>Reach</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="cursor: pointer;">
                            <td><span class="rounded px-2 py-1 me-2" style="background:linear-gradient(135deg,#fdc468 0%,#df4996 50%,#4f5bd5 100%);"><i class="fab fa-instagram" style="color:white;"></i></span>Instagram</td>
                            <td>1,234</td>
                            <td>2,345</td>
                        </tr>
                        <tr style="cursor: pointer;">
                            <td><span class="rounded px-2 py-1 me-2" style="background:#1877F3;"><i class="fab fa-facebook" style="color:white;"></i></span>Facebook</td>
                            <td>1,122</td>
                            <td>2,233</td>
                        </tr>
                        <tr style="cursor: pointer;">
                            <td><span class="rounded px-2 py-1 me-2" style="background:#1DA1F2;"><i class="fab fa-twitter" style="color:white;"></i></span>Twitter</td>
                            <td>1,010</td>
                            <td>2,121</td>      
                        </tr>
                        <tr style="cursor: pointer;">
                            <td><span class="rounded px-2 py-1 me-2" style="background:#0a66c2;"><i class="fab fa-linkedin" style="color:white;"></i></span>LinkedIn</td>
                            <td>800</td>
                            <td>2,010</td>
                        </tr>
                        <tr style="cursor: pointer;">
                            <td><span class="rounded px-2 py-1 me-2" style="background:#000000;"><i class="fab fa-tiktok" style="color:white;"></i></span>TikTok</td>
                            <td>800</td>
                            <td>1,900</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Live Social Media Analytics Dashboard -->
    <div class="card shadow-sm mt-5">
        <div class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="card-title mb-0">Live Social Media Analytics</h5>
                <div class="d-flex align-items-center gap-3">
                    <div class="d-flex align-items-center">
                        <label for="platformSelect" class="form-label me-2 mb-0" style="font-size:0.9rem;">Platform:</label>
                        <select id="platformSelect" class="form-select form-select-sm" style="width:auto;" bind:value={selectedPlatform} on:change={handlePlatformChange}>
                            {#each platforms as platform}
                                <option value={platform}>{platform}</option>
                            {/each}
                        </select>
                    </div>
                    <div class="d-flex align-items-center">
                        <label for="postSelect" class="form-label me-2 mb-0" style="font-size:0.9rem;">Post:</label>
                        <select id="postSelect" class="form-select form-select-sm" style="width:auto;" bind:value={selectedPost} on:change={handlePostChange}>
                            {#each posts as post}
                                <option value={post}>{post}</option>
                            {/each}
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="mb-2">
                <span class="badge bg-primary me-2">{selectedPlatform}</span>
                <span class="badge bg-success me-2">{selectedPost}</span>
            </div>
        
            <div style="background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); padding: 20px;">
                <canvas bind:this={chartCanvas} width="800" height="400"></canvas>
            </div>
            <div class="text-muted mt-2" style="font-size:0.95rem;">
                Real-time analytics showing likes, comments, and shares. Data updates every hour.
            </div>
        </div>
    </div>
</div>