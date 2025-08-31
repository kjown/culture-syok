<script>
    import { onMount, onDestroy } from "svelte";
    import dayGridPlugin from "@fullcalendar/daygrid";
    import timeGridPlugin from "@fullcalendar/timegrid";
    import interactionPlugin from "@fullcalendar/interaction";
    import { Calendar } from "@fullcalendar/core";
    import { selectedDate } from "$lib/stores/userStore.js";
    import PostDetailsModal from "./PostDetailsModal.svelte";

    /** @type {Array<any>} */
    export let calendarEvents = [];

    /** @type {HTMLElement} */
    let calendarEl;
    /** @type {Calendar | null} */
    let calendar = null;
    /** @type {string} */
    let view = "dayGridMonth";
    /** @type {string} */
    let currentTitle = "";
    /** @type {boolean} */
    let showModal = false;
    /** @type {any} */
    let selectedEvent = undefined;

    // Update calendar when events prop changes
    $: if (calendar && calendarEvents) {
        calendar.removeAllEvents();
        calendar.addEventSource(calendarEvents);
    }

    onMount(() => {
        calendar = new Calendar(calendarEl, {
            plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
            initialView: view,
            events: calendarEvents,
            height: "auto",
            headerToolbar: false,
            selectable: true,
            selectMirror: true,
            eventClick: function (/** @type {any} */ info) {
                selectedEvent = {
                    id: info.event.id,
                    title: info.event.title,
                    start: info.event.startStr,
                    content: info.event.extendedProps?.description || "",
                };
                showModal = true;
            },
            dateClick: function (/** @type {any} */ info) {
                selectedDate.set({
                    date: info.dateStr,
                    time: "",
                });
            },
            select: function (/** @type {any} */ info) {
                const startDate = info.start.toISOString().split("T")[0];
                const startTime = info.start.toTimeString().slice(0, 5);

                selectedDate.set({
                    date: startDate,
                    time: startTime,
                });

                if (calendar) {
                    calendar.unselect();
                }
            },
        });
        calendar.render();
        updateTitle();
    });

    function updateTitle() {
        if (calendar) {
            currentTitle = calendar.view.title;
        }
    }

    function goToday() {
        if (calendar) {
            calendar.today();
            updateTitle();
        }
    }

    function goPrev() {
        if (calendar) {
            calendar.prev();
            updateTitle();
        }
    }

    function goNext() {
        if (calendar) {
            calendar.next();
            updateTitle();
        }
    }

    /**
     * @param {string} newView
     */
    function setView(newView) {
        if (calendar) {
            view = newView;
            calendar.changeView(newView);
            updateTitle();
        }
    }

    function closeModal() {
        showModal = false;
        selectedEvent = undefined;
    }

    /**
     * @param {any} e
     */
    function handleEdit(e) {
        // Handle edit logic here
        showModal = false;
    }

    onDestroy(() => {
        if (calendar) {
            calendar.destroy();
        }
    });
</script>

<div class="scheduler-calendar">
    <!-- Calendar Header -->
    <div class="calendar-header">
        <div class="calendar-controls">
            <button
                type="button"
                class="btn btn-today"
                on:click={goToday}
            >
                <i class="fas fa-calendar-day me-2"></i>
                Today
            </button>
            
            <div class="navigation-controls">
                <button type="button" class="btn btn-nav" on:click={goPrev}>
                    <i class="fas fa-chevron-left"></i>
                </button>
                <div class="current-title">
                    {currentTitle}
                </div>
                <button type="button" class="btn btn-nav" on:click={goNext}>
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
            
            <div class="view-selector">
                <button
                    type="button"
                    class="btn btn-view {view === 'dayGridMonth' ? 'active' : ''}"
                    on:click={() => setView("dayGridMonth")}
                >
                    <i class="fas fa-calendar me-1"></i>
                    Month
                </button>
                <button
                    type="button"
                    class="btn btn-view {view === 'timeGridWeek' ? 'active' : ''}"
                    on:click={() => setView("timeGridWeek")}
                >
                    <i class="fas fa-calendar-week me-1"></i>
                    Week
                </button>
                <button
                    type="button"
                    class="btn btn-view {view === 'timeGridDay' ? 'active' : ''}"
                    on:click={() => setView("timeGridDay")}
                >
                    <i class="fas fa-calendar-day me-1"></i>
                    Day
                </button>
            </div>
        </div>
    </div>

    <!-- Calendar Container -->
    <div class="calendar-container">
        <div bind:this={calendarEl}></div>
    </div>

    {#if showModal}
        <PostDetailsModal
            show={showModal}
            event={selectedEvent}
            on:close={closeModal}
            on:edit={handleEdit}
        />
    {/if}
</div>

<style>
    .scheduler-calendar {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .calendar-header {
        padding: 1.5rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }

    .calendar-controls {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .btn-today {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .btn-today:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        color: white;
    }

    .navigation-controls {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: rgba(255, 255, 255, 0.8);
        padding: 0.5rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .btn-nav {
        background: transparent;
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #667eea;
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    .btn-nav:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        transform: scale(1.05);
    }

    .current-title {
        font-weight: 700;
        font-size: 1.25rem;
        color: #2d3748;
        min-width: 180px;
        text-align: center;
        padding: 0 1rem;
    }

    .view-selector {
        display: flex;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        padding: 0.25rem;
        gap: 0.25rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .btn-view {
        background: transparent;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.875rem;
        color: #64748b;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
    }

    .btn-view:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }

    .btn-view.active {
        background: #667eea;
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .calendar-container {
        padding: 2rem;
        min-height: 500px;
    }

    /* Calendar styling overrides */
    :global(.fc) {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    :global(.fc-event) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    :global(.fc-event:hover) {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }

    :global(.fc-day-today) {
        background-color: rgba(102, 126, 234, 0.05) !important;
    }

    :global(.fc-daygrid-day:hover) {
        background-color: rgba(102, 126, 234, 0.02) !important;
    }

    :global(.fc-col-header-cell) {
        background: rgba(102, 126, 234, 0.05) !important;
        border: none !important;
        padding: 1rem 0.5rem !important;
        font-weight: 600 !important;
        color: #667eea !important;
    }

    :global(.fc-daygrid-day-number) {
        color: #2d3748 !important;
        font-weight: 500 !important;
        padding: 0.5rem !important;
    }

    :global(.fc-scrollgrid) {
        border: none !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    :global(.fc-scrollgrid-section > td) {
        border: 1px solid rgba(0, 0, 0, 0.05) !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .calendar-controls {
            flex-direction: column;
            gap: 1rem;
        }

        .navigation-controls {
            order: 1;
        }

        .btn-today {
            order: 2;
        }

        .view-selector {
            order: 3;
        }

        .current-title {
            font-size: 1.1rem;
            min-width: 140px;
        }

        .btn-view {
            padding: 0.5rem 0.75rem;
            font-size: 0.8rem;
        }

        .calendar-header {
            padding: 1rem;
        }

        .calendar-container {
            padding: 1rem;
        }
    }
</style>
