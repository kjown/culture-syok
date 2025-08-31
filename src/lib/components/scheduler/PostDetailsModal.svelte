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
    <div class="modal-backdrop">
        <div class="modal-container">
            <div class="modal-wrapper">
                <!-- Modal Header -->
                <div class="modal-header">
                    <div class="header-content">
                        <div class="header-icon">
                            <i class="fas fa-calendar-alt"></i>
                        </div>
                        <div class="header-text">
                            {#if editing}
                                <div class="title-edit">
                                    <label class="input-label" for="editTitleInput">Post Title</label>
                                    <input
                                        id="editTitleInput"
                                        class="title-input"
                                        bind:value={editTitle}
                                        placeholder="Enter post title..."
                                    />
                                </div>
                            {:else}
                                <h4 class="modal-title">{safeEvent.title}</h4>
                                <p class="modal-subtitle">Scheduled post details</p>
                            {/if}
                        </div>
                    </div>
                    <button
                        type="button"
                        class="close-btn"
                        aria-label="Close"
                        on:click={close}
                    >
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <!-- Modal Body -->
                <div class="modal-body">
                    <div class="datetime-info">
                        <div class="info-item">
                            <i class="fas fa-clock"></i>
                            <span>Scheduled for: {safeEvent.start}</span>
                        </div>
                    </div>

                    {#if editing}
                        <!-- Content Section -->
                        <div class="form-section">
                            <label class="section-label" for="editContentInput">
                                <i class="fas fa-edit"></i>
                                Content
                            </label>
                            <div class="content-wrapper">
                                <textarea
                                    id="editContentInput"
                                    class="content-textarea"
                                    rows="4"
                                    bind:value={editContent}
                                    maxlength={280}
                                    placeholder="What would you like to share?"
                                ></textarea>
                                <div class="character-count">
                                    {editContent.length}/280
                                </div>
                            </div>
                        </div>

                        <!-- Media Section -->
                        <div class="form-section">
                            <label class="section-label">
                                <i class="fas fa-image"></i>
                                Media
                            </label>
                            {#if !editMediaFile}
                                <div
                                    role="button"
                                    tabindex="0"
                                    aria-label="Upload media"
                                    class="media-upload-area"
                                    on:click={() => {
                                        const mediaInput = document.getElementById("editMediaInput");
                                        if (mediaInput) mediaInput.click();
                                    }}
                                    on:keydown={handleKeyDown}
                                    on:drop={handleDrop}
                                    on:dragover={handleDragOver}
                                >
                                    <div class="upload-content">
                                        <div class="upload-icon">
                                            <i class="fas fa-cloud-upload-alt"></i>
                                        </div>
                                        <div class="upload-text">
                                            <p>Drag & drop your media here</p>
                                            <span>or <strong>click to browse</strong></span>
                                        </div>
                                    </div>
                                    <input
                                        id="editMediaInput"
                                        type="file"
                                        accept="image/*,video/*"
                                        class="file-input"
                                        on:change={handleFileChange}
                                    />
                                </div>
                            {:else}
                                <div class="media-preview">
                                    <div class="preview-container">
                                        {#if editMediaType === "image"}
                                            <img
                                                src={editMediaPreview}
                                                alt="Preview"
                                                class="preview-image"
                                            />
                                        {:else if editMediaType === "video"}
                                            <div class="video-placeholder">
                                                <i class="fas fa-play-circle"></i>
                                                <span>Video selected</span>
                                            </div>
                                        {/if}
                                        <button
                                            type="button"
                                            class="remove-media-btn"
                                            aria-label="Remove media"
                                            on:click={removeMedia}
                                        >
                                            <i class="fas fa-times"></i>
                                        </button>
                                    </div>
                                    <div class="media-filename">
                                        <i class="fas fa-file"></i>
                                        {editMediaFile?.name}
                                    </div>
                                </div>
                            {/if}
                        </div>

                        <!-- Schedule Settings -->
                        <div class="schedule-grid">
                            <div class="form-section">
                                <label class="section-label" for="editDateInput">
                                    <i class="fas fa-calendar"></i>
                                    Date
                                </label>
                                <input
                                    type="date"
                                    id="editDateInput"
                                    class="date-input"
                                    bind:value={editDate}
                                />
                            </div>
                            <div class="form-section">
                                <label class="section-label" for="editTimeInput">
                                    <i class="fas fa-clock"></i>
                                    Time
                                </label>
                                <input
                                    type="time"
                                    id="editTimeInput"
                                    class="time-input"
                                    bind:value={editTime}
                                />
                            </div>
                        </div>

                        <!-- Calendar Selection -->
                        <div class="form-section">
                            <label class="section-label" for="editCalendarSelect">
                                <i class="fas fa-calendar-alt"></i>
                                Calendar
                            </label>
                            <select
                                id="editCalendarSelect"
                                class="calendar-select"
                                bind:value={editCalendar}
                            >
                                <option value="">Primary Calendar</option>
                            </select>
                        </div>

                        <!-- Reminder Settings -->
                        <div class="form-section">
                            <div class="reminder-toggle">
                                <input
                                    class="toggle-input"
                                    type="checkbox"
                                    bind:checked={editReminderEnabled}
                                    id="editReminderSwitch"
                                />
                                <label class="toggle-label" for="editReminderSwitch">
                                    <i class="fas fa-bell"></i>
                                    Set Reminder
                                </label>
                            </div>
                            {#if editReminderEnabled}
                                <div class="reminder-options">
                                    <div class="reminder-input-group">
                                        <input
                                            type="number"
                                            min="1"
                                            id="editReminderMinutesInput"
                                            class="reminder-number"
                                            bind:value={editReminderMinutes}
                                        />
                                        <select
                                            id="editReminderTypeSelect"
                                            class="reminder-type"
                                            bind:value={editReminderType}
                                        >
                                            <option value="minutes">minutes before</option>
                                            <option value="hours">hours before</option>
                                        </select>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    {:else}
                        <!-- View Mode -->
                        <div class="content-display">
                            <div class="content-section">
                                <h6 class="content-title">
                                    <i class="fas fa-file-text"></i>
                                    Content
                                </h6>
                                <p class="content-text">{safeEvent.content}</p>
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Modal Footer -->
                <div class="modal-footer">
                    {#if editing}
                        <div class="action-buttons">
                            <button
                                type="button"
                                class="btn btn-save"
                                on:click={saveEdit}
                            >
                                <i class="fas fa-check"></i>
                                Save Changes
                            </button>
                            <button
                                type="button"
                                class="btn btn-cancel"
                                on:click={() => (editing = false)}
                            >
                                <i class="fas fa-times"></i>
                                Cancel
                            </button>
                        </div>
                    {:else}
                        <div class="action-buttons">
                            <button
                                type="button"
                                class="btn btn-edit"
                                on:click={startEdit}
                            >
                                <i class="fas fa-edit"></i>
                                Edit Post
                            </button>
                            <button type="button" class="btn btn-delete">
                                <i class="fas fa-trash"></i>
                                Delete Post
                            </button>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1050;
        padding: 1rem;
    }

    .modal-container {
        width: 100%;
        max-width: 600px;
        max-height: 90vh;
        overflow-y: auto;
    }

    .modal-wrapper {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        overflow: hidden;
    }

    .modal-header {
        padding: 2rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
    }

    .header-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex: 1;
    }

    .header-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        flex-shrink: 0;
    }

    .modal-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .modal-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .title-edit {
        width: 100%;
    }

    .input-label {
        display: block;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }

    .title-input {
        width: 100%;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
    }

    .title-input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }

    .close-btn {
        background: none;
        border: none;
        color: #9ca3af;
        font-size: 1.2rem;
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .close-btn:hover {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }

    .modal-body {
        padding: 2rem;
    }

    .datetime-info {
        background: rgba(102, 126, 234, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .info-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #2d3748;
        font-weight: 500;
    }

    .info-item i {
        color: #667eea;
        width: 16px;
    }

    .form-section {
        margin-bottom: 2rem;
    }

    .section-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
    }

    .section-label i {
        color: #667eea;
        width: 16px;
    }

    .content-wrapper {
        position: relative;
    }

    .content-textarea {
        width: 100%;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        resize: vertical;
        min-height: 120px;
        background: rgba(255, 255, 255, 0.8);
    }

    .content-textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }

    .character-count {
        position: absolute;
        bottom: 0.75rem;
        right: 1rem;
        font-size: 0.8rem;
        color: #9ca3af;
        background: rgba(255, 255, 255, 0.9);
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
    }

    .media-upload-area {
        border: 2px dashed #cbd5e0;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
    }

    .media-upload-area:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
    }

    .upload-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .upload-icon {
        font-size: 2rem;
        color: #667eea;
    }

    .upload-text p {
        margin: 0;
        color: #2d3748;
        font-weight: 500;
    }

    .upload-text span {
        color: #718096;
        font-size: 0.9rem;
    }

    .upload-text strong {
        color: #667eea;
    }

    .file-input {
        display: none;
    }

    .media-preview {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    .preview-container {
        position: relative;
    }

    .preview-image {
        width: 100%;
        height: auto;
        max-height: 200px;
        object-fit: cover;
        display: block;
    }

    .video-placeholder {
        background: #4a5568;
        color: white;
        padding: 3rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .video-placeholder i {
        font-size: 2rem;
    }

    .remove-media-btn {
        position: absolute;
        top: 0.75rem;
        right: 0.75rem;
        background: rgba(239, 68, 68, 0.9);
        border: none;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.8rem;
    }

    .remove-media-btn:hover {
        background: #dc2626;
        transform: scale(1.1);
    }

    .media-filename {
        padding: 0.75rem 1rem;
        background: rgba(0, 0, 0, 0.02);
        color: #718096;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .schedule-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .date-input,
    .time-input,
    .calendar-select {
        width: 100%;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
    }

    .date-input:focus,
    .time-input:focus,
    .calendar-select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }

    .reminder-toggle {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .toggle-input {
        width: 20px;
        height: 20px;
        cursor: pointer;
    }

    .toggle-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        color: #2d3748;
        cursor: pointer;
        margin: 0;
    }

    .reminder-options {
        background: rgba(102, 126, 234, 0.02);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .reminder-input-group {
        display: flex;
        gap: 0.75rem;
    }

    .reminder-number,
    .reminder-type {
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
    }

    .reminder-number {
        flex: 1;
        max-width: 80px;
    }

    .reminder-type {
        flex: 2;
    }

    .reminder-number:focus,
    .reminder-type:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }

    .content-display {
        background: rgba(0, 0, 0, 0.02);
        border-radius: 12px;
        padding: 1.5rem;
    }

    .content-section {
        margin-bottom: 1rem;
    }

    .content-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
    }

    .content-title i {
        color: #667eea;
    }

    .content-text {
        color: #4a5568;
        line-height: 1.6;
        margin: 0;
    }

    .modal-footer {
        padding: 1.5rem 2rem 2rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }

    .action-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
    }

    .btn {
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .btn-save {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }

    .btn-save:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }

    .btn-cancel {
        background: rgba(107, 114, 128, 0.1);
        color: #6b7280;
        border: 1px solid #d1d5db;
    }

    .btn-cancel:hover {
        background: rgba(107, 114, 128, 0.2);
        color: #4b5563;
    }

    .btn-edit {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .btn-edit:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .btn-delete {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }

    .btn-delete:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .modal-backdrop {
            padding: 0.5rem;
        }

        .modal-header {
            padding: 1.5rem 1rem 1rem;
        }

        .modal-body {
            padding: 1.5rem 1rem;
        }

        .modal-footer {
            padding: 1rem;
        }

        .schedule-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .action-buttons {
            flex-direction: column;
        }

        .btn {
            width: 100%;
            justify-content: center;
        }

        .header-content {
            flex-direction: column;
            text-align: center;
        }
    }
</style>
