<script>
    import { onMount } from "svelte";
    import { page } from "$app/stores";
    import { postToSchedule } from "$lib/stores/schedulingStore.js";
    import CreatePostForm from "$lib/components/scheduler/CreatePostForm.svelte";
    import SchedulerCalendar from "$lib/components/scheduler/SchedulerCalendar.svelte";

    /** @type {any} */
    let calendarComponent;
    /** @type {Array<any>} */
    let events = [];
    /** @type {boolean} */
    let isLoading = true;

    // This variable will hold the data from the store to pass as a prop.
    /** @type {{ caption: string; campaign: string; tags: string[] } | null} */
    let prefilledData = null;

    async function fetchEvents() {
        isLoading = true;
        try {
            const response = await fetch("/api/calendar/events");
            if (response.ok) {
                const rawEvents = await response.json();
                events = rawEvents.map((/** @type {any} */ event) => ({
                    id: event.id,
                    title: event.summary,
                    start: event.start.dateTime || event.start.date,
                    end: event.end.dateTime || event.end.date,
                    extendedProps: {
                        description: event.description || "",
                    },
                }));
            } else {
                console.error("Failed to fetch events");
            }
        } catch (error) {
            console.error("Error fetching events:", error);
        }
        isLoading = false;
    }

    onMount(() => {
        // Fetch calendar events when the component mounts
        fetchEvents();

        // Subscribe to the store for pre-filled data from other pages
        const unsubscribe = postToSchedule.subscribe((data) => {
            if (data) {
                prefilledData = data;
                postToSchedule.set(null); // Clear the store after use
            }
        });

        return () => {
            unsubscribe();
        };
    });

    function handlePostsUpdated() {
        // Re-fetch events when a new post is created
        fetchEvents();
    }
</script>

<div class="container py-4">
    <div class="page-header">
        <h1 class="page-title">
            <i class="fas fa-calendar-alt me-3"></i>
            Content Scheduler
        </h1>
        <p class="page-subtitle">
            Schedule and manage your social media content across all platforms
        </p>
    </div>

    <div class="row g-4">
        <div class="col-lg-4">
            <!-- Pass both prefilledData (from store) and approvedIdeas (from load function) -->
            <CreatePostForm
                {prefilledData}
                approvedIdeas={$page.data.approvedIdeas || []}
                on:postsUpdated={handlePostsUpdated}
            />
        </div>
        <div class="col-lg-8">
            <div class="card">
                <div class="card-body">
                    {#if isLoading}
                        <div class="d-flex justify-content-center align-items-center" style="min-height: 400px;">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    {:else}
                        <SchedulerCalendar
                            bind:this={calendarComponent}
                            calendarEvents={events}
                        />
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>

<style>
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

    /* Responsive design */
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
    }
</style>
