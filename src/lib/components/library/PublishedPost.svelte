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

<div class="container py-4">
    <h1 class="mb-2">Published Posts</h1>
    <div class="text-muted mb-3" style="font-size:1.05rem;">
        View all your published posts and their performance
    </div>

    <div class="mb-3">
        <input
            class="form-control"
            type="search"
            placeholder="Search posts"
            bind:value={search}
            style="max-width:400px;"
        />
    </div>

    <div class="d-flex gap-2 mb-3 flex-wrap">
        <select class="form-select w-auto" bind:value={selectedChannel}>
            {#each channels as channel}
                <option value={channel}>{channel}</option>
            {/each}
        </select>
        <select class="form-select w-auto" bind:value={selectedDate}>
            {#each dateRanges as range}
                <option value={range}>{range}</option>
            {/each}
        </select>
        <select class="form-select w-auto" bind:value={selectedSort}>
            {#each sortOptions as sort}
                <option value={sort}>{sort}</option>
            {/each}
        </select>
    </div>

    <div class="card">
        <div class="card-body p-0">
            <table class="table mb-0">
                <thead>
                    <tr>
                        <th>Post</th>
                        <th>Channel</th>
                        <th>Published</th>
                        <th>Impressions</th>
                        <th>Likes</th>
                        <th>Comments</th>
                        <th>Shares</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {#each posts as post}
                        <tr>
                            <td style="max-width:220px;white-space:pre-line;"
                                >{post.content}</td
                            >
                            <td>{post.channel}</td>
                            <td>{post.published}</td>
                            <td>{post.impressions}</td>
                            <td>{post.likes}</td>
                            <td>{post.comments}</td>
                            <td>{post.shares}</td>
                            <td>
                                <button
                                    class="btn btn-link fw-bold text-primary p-0"
                                    type="button"
                                    on:click={() => viewPost(post.id)}
                                >
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
