<script>
    // @ts-nocheck
    import { onMount, onDestroy } from 'svelte';
    
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
    ];
    
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
    let labels = [];
    let likes = [];
    let comments = [];
    let shares = [];
    let totalLikes = 0;
    let totalComments = 0;
    let totalShares = 0;
    let t = 0;
    let chartInterval = null;

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
                            title: { display: true, text: 'Time (s)', color: '#666', font: { size: 14 } },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: { color: '#666' }
                        },
                        y: {
                            title: { display: true, text: 'Count', color: '#666', font: { size: 14 } },
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: { color: '#666' },
                            beginAtZero: true
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
            
            totalLikes += likesIncrease;
            totalComments += commentsIncrease;
            totalShares += sharesIncrease;
            t += 1;

            labels.push(t);
            likes.push(totalLikes);
            comments.push(totalComments);
            shares.push(totalShares);

            if (labels.length > 50) {
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

    onDestroy(() => {
        if (chartInterval) {
            clearInterval(chartInterval);
        }
        if (chart) {
            chart.destroy();
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
    <div class="d-flex mb-3">
        <button class="btn btn-light me-2 active" type="button">Engagement</button>
        <button class="btn btn-light" type="button">Reach</button>
    </div>

    <!-- Engagement Over Time Placeholder -->
    <div class="mb-4">
        <div class="fw-bold" style="font-size:1.3rem;">6,789</div>
        <div class="text-muted mb-2">Last 30 Days <span class="text-success">+10%</span></div>
        <div style="height:120px; background:linear-gradient(90deg,#f5f5fa 60%,#e0e7ef 100%); border-radius:8px; margin-bottom:1rem; display:flex; align-items:end;">
            <!-- Placeholder for chart -->
            <svg width="100%" height="100%" viewBox="0 0 400 100">
                <polyline
                    fill="none"
                    stroke="#2563eb"
                    stroke-width="3"
                    points="10,80 50,40 90,70 130,50 170,60 210,30 250,90 290,60 330,80 370,40"
                />
            </svg>
        </div>
    </div>

    <!-- Top Posts by Engagement Table -->
    <div class="mb-4">
        <div class="fw-bold mb-2">Top Posts by Engagement</div>
        <div class="card">
            <div class="card-body p-0">
                <table class="table mb-0">
                    <thead>
                        <tr>
                            <th>Post</th>
                            <th>Channel</th>
                            <th>Engagement</th>
                            <th>Reach</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span class="rounded bg-light px-2 py-1 me-2">📸</span>Instagram</td>
                            <td>Instagram</td>
                            <td>1,234</td>
                            <td>2,345</td>
                        </tr>
                        <tr>
                            <td><span class="rounded bg-light px-2 py-1 me-2">📘</span>Facebook</td>
                            <td>Facebook</td>
                            <td>1,122</td>
                            <td>2,233</td>
                        </tr>
                        <tr>
                            <td><span class="rounded bg-light px-2 py-1 me-2">🐦</span>Twitter</td>
                            <td>Twitter</td>
                            <td>1,010</td>
                            <td>2,121</td>
                        </tr>
                        <tr>
                            <td><span class="rounded bg-light px-2 py-1 me-2">💼</span>LinkedIn</td>
                            <td>LinkedIn</td>
                            <td>800</td>
                            <td>2,010</td>
                        </tr>
                        <tr>
                            <td><span class="rounded bg-light px-2 py-1 me-2">🎵</span>TikTok</td>
                            <td>TikTok</td>
                            <td>800</td>
                            <td>1,900</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Performance by Channel -->
    <div class="mb-4">
        <div class="fw-bold mb-2">Performance by Channel</div>
        <div class="mb-1" style="font-size:1.3rem;">6,789</div>
        <div class="text-muted mb-2">Last 30 Days <span class="text-success">+10%</span></div>
        <div>
            <div class="mb-2">
                <span class="fw-bold text-primary">Instagram</span>
                <div style="height:10px; background:#e0e7ef; border-radius:5px;">
                    <div style="width:70%; height:10px; background:#2563eb; border-radius:5px;"></div>
                </div>
            </div>
            <div class="mb-2">
                <span class="fw-bold text-primary">Facebook</span>
                <div style="height:10px; background:#e0e7ef; border-radius:5px;">
                    <div style="width:60%; height:10px; background:#2563eb; border-radius:5px;"></div>
                </div>
            </div>
            <div class="mb-2">
                <span class="fw-bold text-primary">Twitter</span>
                <div style="height:10px; background:#e0e7ef; border-radius:5px;">
                    <div style="width:50%; height:10px; background:#2563eb; border-radius:5px;"></div>
                </div>
            </div>
            <div class="mb-2">
                <span class="fw-bold text-primary">LinkedIn</span>
                <div style="height:10px; background:#e0e7ef; border-radius:5px;">
                    <div style="width:90%; height:10px; background:#2563eb; border-radius:5px;"></div>
                </div>
            </div>
            <div class="mb-2">
                <span class="fw-bold text-primary">TikTok</span>
                <div style="height:10px; background:#e0e7ef; border-radius:5px;">
                    <div style="width:40%; height:10px; background:#2563eb; border-radius:5px;"></div>
                </div>
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
                Real-time analytics showing likes, comments, and shares. Data updates every 5 seconds.
            </div>
        </div>
    </div>
</div>