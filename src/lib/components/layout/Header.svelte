<script>
    export let title;
</script>

<nav
    class="navbar navbar-light bg-white border-bottom px-4 py-2 d-flex justify-content-between align-items-center header-sticky"
>
    <div class="d-flex align-items-center gap-2">
        <span class="navbar-brand fw-bold">{title}</span>
    </div>
    <div class="d-flex align-items-center gap-3">
        <a class="nav-link" href="/">Home</a>
        <a class="nav-link" href="/scheduler">Scheduler</a>
        <a class="nav-link" href="/inspiration">Inspiration</a>
        <a class="nav-link" href="/collaborate">Collaborate</a>
        <a class="nav-link" href="/library">Library</a>
        <a class="btn btn-primary" href="/api/auth/google">Connect Google Calendar</a>
        <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuD5ECcReYYZWnYgssqJt_SkajG8H4J3W3qeFVPJUWzzAC7qIY6MHGxj83J4-kj3CVlzFz-mWY-HHEYTZdPWiWZ-qjNvtnbwG8MC1rEoUu-OsxDyAt0gwfyZ4HbCuFslsh9-8eBf5mZCLsWLHsmQtslt0ozDk48-cVsEnzeUjEXTSXahshofjZht-hm8Lv1Fyc1sNeQlUtc1VZvF2jZiTOUDbVfKXF8ZW8DQXUKRbw_5P7ll9IJRYiGvrGS0eX3hbY7pnyfq4st5Y9k"
            alt="User"
            class="rounded-circle"
            width="40"
            height="40"
        />
    </div>
</nav>

<style>
    .header-sticky {
        position: sticky;
        top: 0;
        z-index: 1020;
        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.08),
            0 1px 3px rgba(0, 0, 0, 0.1);
    }
</style>
