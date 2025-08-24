<script>
    import { onMount, onDestroy } from "svelte";
    import dayGridPlugin from "@fullcalendar/daygrid";
    import timeGridPlugin from "@fullcalendar/timegrid";
    import interactionPlugin from "@fullcalendar/interaction";
    import { Calendar } from "@fullcalendar/core";
    import { selectedDate } from "$lib/stores/userStore.js";
    import { events } from "$lib/stores/eventsStore.js";
    import PostDetailsModal from "./PostDetailsModal.svelte";

    /**
     * @typedef {Object} CalendarEvent
     * @property {string} id
     * @property {string} title
     * @property {string} start
     * @property {string} content
     * @property {string} [calendar]
     * @property {boolean} [reminderEnabled]
     * @property {number} [reminderMinutes]
     * @property {string} [reminderType]
     * @property {File|null} [mediaFile]
     * @property {string} [mediaType]
     * @property {string} [mediaPreview]
     */

    /** @type {HTMLElement} */
    let calendarEl;
    /** @type {import('@fullcalendar/core').Calendar|null} */
    let calendar = null;
    /** @type {string} */
    let view = "dayGridMonth";
    /** @type {string} */
    let currentTitle = "";

    /** @type {CalendarEvent[]} */
    let calendarEvents = [];
    const unsubscribe = events.subscribe((evts) => {
        calendarEvents = /** @type {CalendarEvent[]} */ (evts);
        if (calendar) {
            calendar.removeAllEvents();
            calendar.addEventSource(calendarEvents);
        }
    });

    /** @param {string} newView */
    function setView(newView) {
        view = newView;
        if (calendar) {
            calendar.changeView(newView);
            updateTitle();
        }
    }

    function goNext() {
        if (calendar) {
            calendar.next();
            updateTitle();
        }
    }

    function goPrev() {
        if (calendar) {
            calendar.prev();
            updateTitle();
        }
    }

    function goToday() {
        if (calendar) {
            calendar.today();
            updateTitle();
        }
    }

    function updateTitle() {
        if (calendar) {
            currentTitle = calendar.view.title;
        }
    }

    let showModal = false;
    /** @type {CalendarEvent | undefined} */
    let selectedEvent = undefined;

    onMount(() => {
        calendar = new Calendar(calendarEl, {
            plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
            initialView: view,
            events: calendarEvents,
            height: "auto",
            headerToolbar: false,
            selectable: true,
            selectMirror: true,
            eventClick: function (info) {
                // Open modal and pass event details
                selectedEvent = {
                    id: info.event.id,
                    title: info.event.title,
                    start: info.event.startStr,
                    content: info.event.extendedProps?.content || "",
                    calendar: typeof info.event.extendedProps?.calendar === "string"
                        ? info.event.extendedProps.calendar
                        : "",
                    reminderEnabled:
                        info.event.extendedProps?.reminderEnabled ?? false,
                    reminderMinutes:
                        info.event.extendedProps?.reminderMinutes ?? 10,
                    reminderType:
                        info.event.extendedProps?.reminderType || "minutes",
                    mediaFile: info.event.extendedProps?.mediaFile ?? null,
                    mediaType: info.event.extendedProps?.mediaType || "",
                    mediaPreview: info.event.extendedProps?.mediaPreview || "",
                };
                showModal = true;
            },
            dateClick: function (info) {
                // Only date (month view all-day), clear time
                selectedDate.set({
                    date: info.dateStr,
                    time: "",
                });
            },
            select: function (info) {
                // Handle time slot selection in week/day views
                const startDate = info.start.toISOString().split("T")[0];
                const startTime = info.start.toTimeString().slice(0, 5);

                selectedDate.set({
                    date: startDate,
                    time: startTime,
                });

                // Clear the selection
                if (calendar) {
                    calendar.unselect();
                }
            },
        });
        calendar.render();
        updateTitle();
    });

    function closeModal() {
        showModal = false;
        selectedEvent = undefined;
    }

    /**
     * @param {CustomEvent<CalendarEvent>} e
     */
    function handleEdit(e) {
        const updated = e.detail;
        events.update((evts) =>
            evts.map((ev) =>
                ev.id === updated.id ? { ...ev, ...updated } : ev,
            ),
        );
        selectedEvent = updated;
        showModal = false;
    }

    onDestroy(() => {
        if (calendar) {
            calendar.destroy();
        }
        unsubscribe();
    });
</script>

<div>
    <!-- Calendar Header: All controls in a horizontal row -->
    <div
        class="d-flex align-items-center justify-content-between gap-3 mb-3 flex-wrap"
    >
        <!-- Today Button -->
        <button
            type="button"
            class="btn btn-outline-secondary"
            on:click={goToday}
            title="Today"
        >
            Today
        </button>
        <!-- Navigation Arrows -->
        <button
            type="button"
            class="btn btn-light border"
            on:click={goPrev}
            title="Previous"
            aria-label="Previous month"
        >
            &lt;
        </button>
        <!-- Month/Year Title -->
        <span
            class="fw-bold fs-5 px-3"
            style="min-width: 160px; text-align: center;">{currentTitle}</span
        >
        <!-- Navigation Arrows -->
        <button
            type="button"
            class="btn btn-light border"
            on:click={goNext}
            title="Next"
            aria-label="Next month"
        >
            &gt;
        </button>
        <!-- View Switcher -->
        <div class="btn-group" role="group">
            <button
                type="button"
                class="btn btn-outline-primary {view === 'dayGridMonth'
                    ? 'active'
                    : ''}"
                on:click={() => setView("dayGridMonth")}>Month</button
            >
            <button
                type="button"
                class="btn btn-outline-primary {view === 'timeGridWeek'
                    ? 'active'
                    : ''}"
                on:click={() => setView("timeGridWeek")}>Week</button
            >
            <button
                type="button"
                class="btn btn-outline-primary {view === 'timeGridDay'
                    ? 'active'
                    : ''}"
                on:click={() => setView("timeGridDay")}>Day</button
            >
        </div>
    </div>
    <div class="calendar-scrollable">
        <div class="border rounded p-2 bg-white" style="min-height: 400px;">
            <div bind:this={calendarEl}></div>
        </div>
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
