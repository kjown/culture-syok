<script>
    import { createEventDispatcher } from "svelte";

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

    /** @type {boolean} */
    export let show = false;
    /** @type {CalendarEvent | undefined} */
    export let event = undefined;

    const dispatch = createEventDispatcher();
    let editing = false;

    // Provide default values when event is undefined
    $: safeEvent = event || {
        id: "",
        title: "",
        start: "",
        content: "",
        calendar: "",
        reminderEnabled: false,
        reminderMinutes: 10,
        reminderType: "minutes",
        mediaFile: null,
        mediaType: "",
        mediaPreview: "",
    };

    // Editable fields with safe defaults
    /** @type {string} */ let editTitle = "";
    /** @type {string} */ let editContent = "";
    /** @type {string} */ let editDate = "";
    /** @type {string} */ let editTime = "";
    /** @type {string} */ let editCalendar = "";
    /** @type {boolean} */ let editReminderEnabled = false;
    /** @type {number} */ let editReminderMinutes = 10;
    /** @type {string} */ let editReminderType = "minutes";
    /** @type {File|null} */ let editMediaFile = null;
    /** @type {string} */ let editMediaType = "";
    /** @type {string} */ let editMediaPreview = "";

    $: if (show && safeEvent && !editing) {
        editTitle = safeEvent.title || "";
        editContent = safeEvent.content || "";
        editDate = safeEvent.start ? safeEvent.start.split("T")[0] : "";
        editTime =
            safeEvent.start && safeEvent.start.includes("T")
                ? safeEvent.start.split("T")[1].slice(0, 5)
                : "";
        editCalendar = safeEvent.calendar || "";
        editReminderEnabled = safeEvent.reminderEnabled || false;
        editReminderMinutes = safeEvent.reminderMinutes || 10;
        editReminderType = safeEvent.reminderType || "minutes";
        editMediaFile = safeEvent.mediaFile || null;
        editMediaType = safeEvent.mediaType || "";
        editMediaPreview = safeEvent.mediaPreview || "";
    }

    function close() {
        dispatch("close");
        editing = false;
    }

    function startEdit() {
        editing = true;
    }

    function saveEdit() {
        let start = editDate;
        if (editTime) start += `T${editTime}`;
        dispatch("edit", {
            ...event,
            title: editTitle,
            content: editContent,
            start,
            calendar: editCalendar,
            reminderEnabled: editReminderEnabled,
            reminderMinutes: editReminderMinutes,
            reminderType: editReminderType,
            mediaFile: editMediaFile,
            mediaType: editMediaType,
            mediaPreview: editMediaPreview,
        });
        editing = false;
    }

    /** @param {File} file */
    function processFile(file) {
        editMediaFile = file;
        editMediaType = file.type.startsWith("image")
            ? "image"
            : file.type.startsWith("video")
              ? "video"
              : "";
        const reader = new FileReader();
        reader.onload = (e) => {
            const result = e.target?.result;
            editMediaPreview = typeof result === "string" ? result : "";
        };
        reader.readAsDataURL(file);
    }

    /** @param {Event} event */
    function handleFileChange(event) {
        const input = /** @type {HTMLInputElement} */ (event.target);
        if (!input || !input.files || !input.files[0]) return;
        const file = input.files[0];
        processFile(file);
    }

    function removeMedia() {
        editMediaFile = null;
        editMediaPreview = "";
        editMediaType = "";
    }

    /** @param {DragEvent} event */
    function handleDragOver(event) {
        event.preventDefault();
    }

    /** @param {DragEvent} event */
    function handleDrop(event) {
        event.preventDefault();
        const file = event.dataTransfer?.files[0];
        if (file) {
            processFile(file);
        }
    }

    /** @param {KeyboardEvent} event */
    function handleKeyDown(event) {
        if (event.key === "Enter" || event.key === " ") {
            const mediaInput = document.getElementById("editMediaInput");
            if (mediaInput) mediaInput.click();
        }
    }
</script>

{#if show && safeEvent}
    <div
        class="modal fade show d-block"
        tabindex="-1"
        style="background: rgba(0,0,0,0.4);"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">
                        {#if editing}
                            <div class="mb-2">
                                <label class="form-label" for="editTitleInput"
                                    >Title</label
                                >
                                <input
                                    id="editTitleInput"
                                    class="form-control"
                                    bind:value={editTitle}
                                />
                            </div>
                        {:else}
                            {safeEvent.title}
                        {/if}
                    </h5>
                    <button
                        type="button"
                        class="btn-close"
                        aria-label="Close"
                        on:click={close}
                    ></button>
                </div>
                <div class="modal-body">
                    <p><strong>Date & Time:</strong> {safeEvent.start}</p>
                    {#if editing}
                        <!-- Content Input -->
                        <div class="mb-3">
                            <label class="form-label" for="editContentInput"
                                >Content</label
                            >
                            <textarea
                                id="editContentInput"
                                class="form-control"
                                rows="4"
                                bind:value={editContent}
                                maxlength={280}
                                placeholder="Write your post here..."
                            ></textarea>
                        </div>
                        <!-- Media Upload Area -->
                        <div class="mb-3">
                            <label class="form-label" for="editMediaInput"
                                >Media</label
                            >
                            {#if !editMediaFile}
                                <div
                                    role="button"
                                    tabindex="0"
                                    aria-label="Upload media"
                                    class="border border-2 border-dashed rounded p-4 text-center text-muted"
                                    style="cursor: pointer;"
                                    on:click={() => {
                                        const mediaInput =
                                            document.getElementById(
                                                "editMediaInput",
                                            );
                                        if (mediaInput) mediaInput.click();
                                    }}
                                    on:keydown={handleKeyDown}
                                    on:drop={handleDrop}
                                    on:dragover={handleDragOver}
                                >
                                    Drag &amp; drop your image/video here, or <span
                                        class="text-primary"
                                        >click to browse</span
                                    >.
                                    <input
                                        id="editMediaInput"
                                        type="file"
                                        accept="image/*,video/*"
                                        class="d-none"
                                        on:change={handleFileChange}
                                    />
                                </div>
                            {:else}
                                <div class="position-relative mb-2">
                                    {#if editMediaType === "image"}
                                        <img
                                            src={editMediaPreview}
                                            alt="Preview"
                                            class="img-thumbnail"
                                            style="max-height: 120px;"
                                        />
                                    {:else if editMediaType === "video"}
                                        <div
                                            class="bg-secondary d-flex align-items-center justify-content-center"
                                            style="height:120px;"
                                        >
                                            <span class="text-white"
                                                >Video selected</span
                                            >
                                        </div>
                                    {/if}
                                    <button
                                        type="button"
                                        class="btn-close position-absolute top-0 end-0 m-2"
                                        aria-label="Remove"
                                        on:click={removeMedia}
                                    ></button>
                                </div>
                                <div class="small text-muted">
                                    {editMediaFile?.name}
                                </div>
                            {/if}
                        </div>
                        <!-- Date Picker -->
                        <div class="mb-3">
                            <label class="form-label" for="editDateInput"
                                >Date</label
                            >
                            <input
                                type="date"
                                id="editDateInput"
                                class="form-control"
                                bind:value={editDate}
                            />
                        </div>
                        <!-- Time Picker -->
                        <div class="mb-3">
                            <label class="form-label" for="editTimeInput"
                                >Time</label
                            >
                            <input
                                type="time"
                                id="editTimeInput"
                                class="form-control"
                                bind:value={editTime}
                            />
                        </div>
                        <!-- Calendar Selection -->
                        <div class="mb-3">
                            <label class="form-label" for="editCalendarSelect"
                                >Select Calendar</label
                            >
                            <select
                                id="editCalendarSelect"
                                class="form-select"
                                bind:value={editCalendar}
                            >
                                <option value="">Primary Calendar</option>
                                <!-- Populate with user's calendars after auth -->
                            </select>
                        </div>
                        <!-- Reminder Configuration -->
                        <div class="mb-3">
                            <div class="form-check form-switch">
                                <input
                                    class="form-check-input"
                                    type="checkbox"
                                    bind:checked={editReminderEnabled}
                                    id="editReminderSwitch"
                                />
                                <label
                                    class="form-check-label"
                                    for="editReminderSwitch">Set Reminder</label
                                >
                            </div>
                            {#if editReminderEnabled}
                                <div class="d-flex gap-2 mt-2">
                                    <label
                                        class="form-label"
                                        for="editReminderMinutesInput"
                                        >Minutes/Hours</label
                                    >
                                    <input
                                        type="number"
                                        min="1"
                                        id="editReminderMinutesInput"
                                        class="form-control w-50"
                                        bind:value={editReminderMinutes}
                                    />
                                    <label
                                        class="form-label ms-2"
                                        for="editReminderTypeSelect">Type</label
                                    >
                                    <select
                                        id="editReminderTypeSelect"
                                        class="form-select w-50"
                                        bind:value={editReminderType}
                                    >
                                        <option value="minutes"
                                            >minutes before</option
                                        >
                                        <option value="hours"
                                            >hours before</option
                                        >
                                    </select>
                                </div>
                            {/if}
                        </div>
                    {:else}
                        <p>{safeEvent.content}</p>
                        <!-- You can show other fields here if you want -->
                    {/if}
                </div>
                <div class="modal-footer">
                    {#if editing}
                        <button
                            type="button"
                            class="btn btn-primary"
                            on:click={saveEdit}>Save</button
                        >
                        <button
                            type="button"
                            class="btn btn-outline-secondary"
                            on:click={() => (editing = false)}>Cancel</button
                        >
                    {:else}
                        <button
                            type="button"
                            class="btn btn-secondary"
                            on:click={startEdit}>Edit</button
                        >
                        <button type="button" class="btn btn-danger"
                            >Delete</button
                        >
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}
