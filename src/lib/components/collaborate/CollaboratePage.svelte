<script>
    let ideas = [
        { image: "/images/idea1.png" },
        { image: "/images/idea2.png" },
        { image: "/images/idea3.png" },
    ];
    let activeTab = "Ideas";
    let tabs = ["Ideas", "To Do", "In Review", "Approved"];
    let link = "";
    let date = "";
    let time = "";
    let reminder = "";
</script>

<div class="container-fluid py-4">
    <div class="row">
        <!-- Left Sidebar: Content Plan Form -->
        <!-- <div class="col-md-3">
            <h3 class="mb-3">Content Plan</h3>
            <div class="mb-3">
                <textarea class="form-control mb-2" rows="4" placeholder="Add a link" bind:value={link}></textarea>
            </div>
            <div class="mb-3">
                <label class="form-label">Schedule</label>
                <input type="date" class="form-control mb-2" bind:value={date} placeholder="Select a date" />
                <input type="time" class="form-control mb-2" bind:value={time} placeholder="Select a time" />
            </div>
            <div class="mb-3">
                <label class="form-label">Reminders</label>
                <input type="text" class="form-control mb-2" bind:value={reminder} placeholder="Add a reminder" />
            </div>
            <button class="btn btn-primary w-100">Schedule Post</button>
        </div> -->

        <!-- Main Content: Content Plan Board -->
        <div class="col-md-9">
            <h3 class="mb-3">Content Plan</h3>
            <ul class="nav nav-tabs mb-3">
                {#each tabs as tab}
                    <li class="nav-item">
                        <button
                            class="nav-link {activeTab === tab ? 'active' : ''}"
                            type="button"
                            on:click={() => (activeTab = tab)}
                        >
                            {tab}
                        </button>
                    </li>
                {/each}
            </ul>
            <div>
                {#each ideas as idea}
                    <div class="mb-4">
                        <img
                            src={idea.image}
                            alt="Idea"
                            class="img-fluid rounded"
                            style="width:100%;height:160px;object-fit:cover;"
                        />
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .nav-tabs .nav-link {
        border: none;
        color: #007bff;
        font-weight: 500;
    }

    .nav-tabs .nav-link.active {
        color: #495057;
        background-color: #e9ecef;
        border-radius: 0.25rem 0.25rem 0 0;
    }

    .nav-tabs {
        border-bottom: 1px solid #dee2e6;
    }

    .container-fluid {
        max-width: 1200px;
        margin: 0 auto;
    }

    @media (max-width: 768px) {
        .col-md-3,
        .col-md-9 {
            width: 100%;
            display: block;
        }

        .nav-tabs {
            display: flex;
            flex-wrap: wrap;
            border: none;
            margin-bottom: 1rem;
        }

        .nav-tabs .nav-item {
            flex: 1 1 auto;
        }
    }
</style>
