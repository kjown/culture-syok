<script>
    import { onMount } from "svelte";
    import CreatePostForm from "$lib/components/scheduler/CreatePostForm.svelte";
    import SchedulerCalendar from "$lib/components/scheduler/SchedulerCalendar.svelte";

    /** @type {any} */
    let calendarComponent;
    /** @type {Array<any>} */
    let events = [];
    /** @type {boolean} */
    let isLoading = true;

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

    onMount(fetchEvents);

    function handlePostsUpdated() {
        fetchEvents();
    }
</script>

<div class="container py-4">
    <h1 class="mb-4">Content Scheduler</h1>

    <div class="row g-4">
        <div class="col-lg-4">
            <CreatePostForm on:postsUpdated={handlePostsUpdated} />
        </div>
        <div class="col-lg-8">
            <div class="card">
                <div class="card-body">
                    {#if isLoading}
                        <p>Loading Calendar...</p>
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
