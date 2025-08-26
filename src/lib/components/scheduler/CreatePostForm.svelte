<script>
    import { selectedDate } from "$lib/stores/userStore.js";
    import { events } from "$lib/stores/eventsStore.js";
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    /**
     * @typedef {Object} CalendarEvent
     * @property {string} id
     * @property {string} title
     * @property {string} start
     */

    let content = "";
    let charCount = 0;
    let calendar = "";
    let reminderEnabled = false;
    let reminderMinutes = 10;
    let reminderType = "minutes";
    const maxChars = 280;

    /** @type {File|null} */
    let mediaFile = null;
    /** @type {string} */
    let mediaPreview = "";
    let mediaType = "";
    let isUploading = false;

    let postTitle = "";
    let postContent = "";
    let scheduleDate = "";
    let isSubmitting = false;

    // Use $selectedDate directly for date and time fields
    $: date = $selectedDate.date;
    $: time = $selectedDate.time;

    function clearForm() {
        postTitle = "";
        content = "";
        charCount = 0;
        calendar = "";
        reminderEnabled = false;
        reminderMinutes = 10;
        reminderType = "minutes";
        removeMedia();
        // Optionally clear selectedDate store
        selectedDate.set({ date: "", time: "" });
    }

    /** @param {File} file */
    function processFile(file) {
        mediaFile = file;
        mediaType = file.type.startsWith("image")
            ? "image"
            : file.type.startsWith("video")
              ? "video"
              : "";
        const reader = new FileReader();
        reader.onload = (e) => {
            const result = e.target?.result;
            mediaPreview = typeof result === "string" ? result : "";
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

    /** @param {DragEvent} event */
    function handleDrop(event) {
        event.preventDefault();
        const file = event.dataTransfer?.files[0];
        if (file) {
            processFile(file);
        }
    }

    function removeMedia() {
        mediaFile = null;
        mediaPreview = "";
        mediaType = "";
    }

    /** @param {DragEvent} event */
    function handleDragOver(event) {
        event.preventDefault();
    }

    /** @param {KeyboardEvent} event */
    function handleKeyDown(event) {
        if (event.key === "Enter" || event.key === " ") {
            const mediaInput = /** @type {HTMLInputElement} */ (
                document.getElementById("mediaInput")
            );
            if (mediaInput) mediaInput.click();
        }
    }

    /** @param {Event} event */
    function handleSubmit(event) {
        event.preventDefault();

        // Only add if title, content and date are present
        if (!postTitle || !content || !date) return;

        // Compose ISO datetime string for start
        let start = date;
        if (time) start += `T${time}`;

        // Add new event to the store
        events.update((evts) => [
            ...evts,
            {
                id: Date.now().toString(),
                title: postTitle,
                start,
                content,
            },
        ]);

        clearForm();
    }

    async function handleSchedule() {
        if (!postContent || !scheduleDate) {
            alert('Please fill in both the content and the schedule date.');
            return;
        }
        isSubmitting = true;

        const startTime = new Date(scheduleDate);
        const endTime = new Date(startTime.getTime() + 30 * 60000);

        const response = await fetch('/api/calendar/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                summary: `[Social Post] ${postContent.substring(0, 30)}...`,
                description: postContent,
                start: startTime.toISOString(),
                end: endTime.toISOString()
            })
        });

        isSubmitting = false;
        if (response.ok) {
            alert('Post scheduled successfully!');
            postContent = '';
            scheduleDate = '';
            dispatch('postsUpdated');
        } else {
            const result = await response.json();
            alert(`Error: ${result.error}`);
        }
    }
</script>

<!-- <div class="form-scrollable">
    <h3 class="fw-bold mb-3">Create a New Post</h3>
    <form on:submit|preventDefault={handleSubmit}>
        <div class="mb-3">
            <label class="form-label" for="titleInput">Title</label>
            <input
                id="titleInput"
                class="form-control"
                type="text"
                bind:value={postTitle}
                maxlength={100}
                placeholder="Enter post title..."
            />
        </div>

        <div class="mb-3">
            <label class="form-label" for="contentInput">Content</label>
            <textarea
                id="contentInput"
                class="form-control"
                rows="4"
                bind:value={content}
                maxlength={maxChars}
                on:input={() => (charCount = content.length)}
                placeholder="Write your post here..."
            ></textarea>
            <small class="text-muted">{charCount}/{maxChars} characters</small>
        </div>

        <div class="mb-3">
            <label class="form-label" for="mediaInput">Media</label>
            {#if !mediaFile}
                <div
                    role="button"
                    tabindex="0"
                    aria-label="Upload media"
                    class="border border-2 border-dashed rounded p-4 text-center text-muted"
                    style="cursor: pointer;"
                    on:click={() => {
                        const mediaInput =
                            document.getElementById("mediaInput");
                        if (mediaInput) mediaInput.click();
                    }}
                    on:keydown={handleKeyDown}
                    on:drop={handleDrop}
                    on:dragover={handleDragOver}
                >
                    Drag &amp; drop your image/video here, or <span
                        class="text-primary">click to browse</span
                    >.
                    <input
                        id="mediaInput"
                        type="file"
                        accept="image/*,video/*"
                        class="d-none"
                        on:change={handleFileChange}
                    />
                </div>
            {:else}
                <div class="position-relative mb-2">
                    {#if isUploading}
                        <div
                            class="position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center bg-white bg-opacity-75"
                        >
                            <div
                                class="spinner-border text-primary"
                                role="status"
                            ></div>
                        </div>
                    {/if}
                    {#if mediaType === "image"}
                        <img
                            src={mediaPreview}
                            alt="Preview"
                            class="img-thumbnail"
                            style="max-height: 120px;"
                        />
                    {:else if mediaType === "video"}
                        <div
                            class="bg-secondary d-flex align-items-center justify-content-center"
                            style="height:120px;"
                        >
                            <span class="text-white">Video selected</span>
                        </div>
                    {/if}
                    <button
                        type="button"
                        class="btn-close position-absolute top-0 end-0 m-2"
                        aria-label="Remove"
                        on:click={removeMedia}
                    ></button>
                </div>
                <div class="small text-muted">{mediaFile?.name}</div>
            {/if}
        </div>

        <div class="mb-3">
            <label class="form-label" for="dateInput">Date</label>
            <input
                type="date"
                id="dateInput"
                class="form-control"
                bind:value={date}
                on:input={() => selectedDate.set({ date, time })}
            />
        </div>
        <div class="mb-3">
            <label class="form-label" for="timeInput">Time</label>
            <input
                type="time"
                id="timeInput"
                class="form-control"
                bind:value={time}
                on:input={() => selectedDate.set({ date, time })}
            />
        </div>
        <div class="mb-3">
            <label class="form-label" for="calendarSelect"
                >Select Calendar</label
            >
            <select
                id="calendarSelect"
                class="form-select"
                bind:value={calendar}
            >
                <option value="">Primary Calendar</option>
            </select>
        </div>
        <div class="mb-3">
            <div class="form-check form-switch">
                <input
                    class="form-check-input"
                    type="checkbox"
                    bind:checked={reminderEnabled}
                    id="reminderSwitch"
                />
                <label class="form-check-label" for="reminderSwitch"
                    >Set Reminder</label
                >
            </div>
            {#if reminderEnabled}
                <div class="d-flex gap-2 mt-2">
                    <label class="form-label" for="reminderMinutesInput"
                        >Minutes/Hours</label
                    >
                    <input
                        type="number"
                        min="1"
                        id="reminderMinutesInput"
                        class="form-control w-50"
                        bind:value={reminderMinutes}
                    />
                    <label class="form-label ms-2" for="reminderTypeSelect"
                        >Type</label
                    >
                    <select
                        id="reminderTypeSelect"
                        class="form-select w-50"
                        bind:value={reminderType}
                    >
                        <option value="minutes">minutes before</option>
                        <option value="hours">hours before</option>
                    </select>
                </div>
            {/if}
        </div>
        <div class="d-flex justify-content-end gap-2 mt-4">
            <button type="submit" class="btn btn-primary">Schedule Post</button>
            <button
                type="button"
                class="btn btn-outline-secondary"
                on:click={clearForm}>Clear Form</button
            >
        </div>
    </form>
</div> -->

<div class="card">
    <div class="card-body">
        <h5 class="card-title">Create a New Post</h5>
        <form on:submit|preventDefault={handleSchedule}>
            <div class="mb-3">
                <label for="postContent" class="form-label">Content</label>
                <textarea
                    class="form-control"
                    id="postContent"
                    rows="4"
                    bind:value={postContent}
                ></textarea>
            </div>
            <div class="mb-3">
                <label for="scheduleDate" class="form-label"
                    >Schedule Date & Time</label
                >
                <input
                    type="datetime-local"
                    class="form-control"
                    id="scheduleDate"
                    bind:value={scheduleDate}
                />
            </div>
            <button
                type="submit"
                class="btn btn-primary"
                disabled={isSubmitting}
            >
                {isSubmitting ? "Scheduling..." : "Schedule Post"}
            </button>
        </form>
    </div>
</div>
