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

<div>
    <!-- Calendar Header -->
    <div
        class="d-flex align-items-center justify-content-between gap-3 mb-3 flex-wrap"
    >
        <button
            type="button"
            class="btn btn-outline-secondary"
            on:click={goToday}
        >
            Today
        </button>
        <button type="button" class="btn btn-light border" on:click={goPrev}>
            &lt;
        </button>
        <span
            class="fw-bold fs-5 px-3"
            style="min-width: 160px; text-align: center;"
        >
            {currentTitle}
        </span>
        <button type="button" class="btn btn-light border" on:click={goNext}>
            &gt;
        </button>
        <div class="btn-group" role="group">
            <button
                type="button"
                class="btn btn-outline-primary {view === 'dayGridMonth'
                    ? 'active'
                    : ''}"
                on:click={() => setView("dayGridMonth")}
            >
                Month
            </button>
            <button
                type="button"
                class="btn btn-outline-primary {view === 'timeGridWeek'
                    ? 'active'
                    : ''}"
                on:click={() => setView("timeGridWeek")}
            >
                Week
            </button>
            <button
                type="button"
                class="btn btn-outline-primary {view === 'timeGridDay'
                    ? 'active'
                    : ''}"
                on:click={() => setView("timeGridDay")}
            >
                Day
            </button>
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
