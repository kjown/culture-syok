<script>
    let powerBIUrl = "https://app.powerbi.com/view?r=YOUR_REPORT_ID";
    let selectedRange = "Last 30 days";
    let ranges = ["Last 7 days", "Last 30 days", "Last 90 days"];
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

    <!-- PowerBI Embed Placeholder -->
    <div class="card shadow-sm mt-5">
        <div class="card-body">
            <h5 class="card-title">PowerBI Analytics</h5>
            <div class="ratio ratio-16x9" style="background:#f5f5fa; border-radius:8px;">
                <iframe
                    src={powerBIUrl}
                    title="PowerBI Dashboard"
                    allowfullscreen
                    style="width:100%;height:100%;border:0;"
                ></iframe>
            </div>
            <div class="text-muted mt-2" style="font-size:0.95rem;">
                Your PowerBI analytics will appear here. Replace the embed URL with your own report.
            </div>
        </div>
    </div>
</div>