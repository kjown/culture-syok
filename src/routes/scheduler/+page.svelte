<script>
    import CreatePostForm from "$lib/components/scheduler/CreatePostForm.svelte";
    import SchedulerCalendar from "$lib/components/scheduler/SchedulerCalendar.svelte";
</script>

<div class="row g-4">
    <!-- Left Panel: Post Creation Form -->
    <div class="col-md-4">
        <CreatePostForm />
    </div>
    <!-- Right Panel: Calendar View -->
    <div class="col-md-8">
        <SchedulerCalendar />
    </div>
</div>
