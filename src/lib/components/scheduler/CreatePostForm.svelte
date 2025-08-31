<script>
    import { createEventDispatcher } from "svelte";
    import MediaUploader from "./MediaUploader.svelte";

    const dispatch = createEventDispatcher();

    let postContent = "";
    let scheduleDate = "";
    /** @type {string} */
    let mediaUrl = "";
    let isSubmitting = false;
    /** @type {import("./MediaUploader.svelte").default|null} */
    let mediaUploaderRef = null; // Used to reset MediaUploader

    // New state variables
    /** @type {string[]} */
    let channels = [];
    let altText = "";
    let campaign = "";
    let tags = "";
    let firstComment = "";

    /**
     * @param {CustomEvent<string|null>} event
     */
    function handleUploadComplete(event) {
        mediaUrl = event.detail || "";
    }

    async function handleSchedule() {
        if (!postContent || !scheduleDate) {
            alert("Please fill in both the content and the schedule date.");
            return;
        }
        isSubmitting = true;

        const startTime = new Date(scheduleDate);
        const endTime = new Date(startTime.getTime() + 30 * 60000);

        // Build structured description
        /** @type {string[]} */
        const descriptionParts = [];
        if (mediaUrl) {
            descriptionParts.push(`[MEDIA_URL]: ${mediaUrl}`);
        }
        if (channels.length > 0) {
            descriptionParts.push(`[CHANNELS]: ${channels.join(", ")}`);
        }
        if (altText) {
            descriptionParts.push(`[ALT_TEXT]: ${altText}`);
        }
        if (campaign) {
            descriptionParts.push(`[CAMPAIGN]: ${campaign}`);
        }
        if (tags) {
            descriptionParts.push(`[TAGS]: ${tags}`);
        }
        if (firstComment) {
            descriptionParts.push(`[FIRST_COMMENT]: ${firstComment}`);
        }

        const metadataString = descriptionParts.join("\n");
        const description = metadataString
            ? `${metadataString}\n---\n${postContent}`
            : postContent;

        const response = await fetch("/api/calendar/events", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                summary: `[Social Post] ${postContent.substring(0, 30)}...`,
                description: description,
                start: startTime.toISOString(),
                end: endTime.toISOString(),
            }),
        });

        isSubmitting = false;
        if (response.ok) {
            alert("Post scheduled successfully!");
            // Reset all form state
            postContent = "";
            scheduleDate = "";
            mediaUrl = "";
            if (mediaUploaderRef && typeof mediaUploaderRef.reset === "function") {
                mediaUploaderRef.reset();
            }
            channels = [];
            altText = "";
            campaign = "";
            tags = "";
            firstComment = "";
            dispatch("postsUpdated");
        } else {
            const result = await response.json();
            alert(`Error: ${result.error}`);
        }
    }
</script>

<div class="create-post-form">
    <div class="form-header">
        <div class="header-icon">
            <i class="fas fa-plus-circle"></i>
        </div>
        <div>
            <h5 class="form-title">Create New Post</h5>
            <p class="form-subtitle">Schedule your content across social platforms</p>
        </div>
    </div>

    <form on:submit|preventDefault={handleSchedule} class="post-form">
        <!-- Content Section -->
        <div class="form-section">
            <label for="postContent" class="form-label">
                <i class="fas fa-edit me-2"></i>
                Content
            </label>
            <div class="content-wrapper">
                <textarea
                    class="form-control content-textarea"
                    id="postContent"
                    rows="4"
                    placeholder="What's on your mind? Write your post content here..."
                    bind:value={postContent}
                ></textarea>
                <div class="character-count">
                    {postContent.length}/280
                </div>
            </div>
        </div>

        <!-- Media Upload Section -->
        <div class="form-section">
            <label class="form-label">
                <i class="fas fa-image me-2"></i>
                Media Upload
            </label>
            <MediaUploader
                bind:this={mediaUploaderRef}
                on:uploadComplete={handleUploadComplete}
            />
        </div>

        <!-- Channels Section -->
        <div class="form-section">
            <label class="form-label">
                <i class="fas fa-share-alt me-2"></i>
                Social Platforms
            </label>
            <div class="channels-grid">
                <div class="channel-item">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        id="facebook"
                        value="Facebook"
                        bind:group={channels}
                    />
                    <label class="channel-label" for="facebook">
                        <div class="channel-icon facebook">
                            <i class="fab fa-facebook-f"></i>
                        </div>
                        <span>Facebook</span>
                    </label>
                </div>
                <div class="channel-item">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        id="instagram"
                        value="Instagram"
                        bind:group={channels}
                    />
                    <label class="channel-label" for="instagram">
                        <div class="channel-icon instagram">
                            <i class="fab fa-instagram"></i>
                        </div>
                        <span>Instagram</span>
                    </label>
                </div>
                <div class="channel-item">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        id="x"
                        value="X"
                        bind:group={channels}
                    />
                    <label class="channel-label" for="x">
                        <div class="channel-icon x">
                            <i class="fab fa-x-twitter"></i>
                        </div>
                        <span>X</span>
                    </label>
                </div>
                <div class="channel-item">
                    <input
                        class="form-check-input"
                        type="checkbox"
                        id="linkedin"
                        value="LinkedIn"
                        bind:group={channels}
                    />
                    <label class="channel-label" for="linkedin">
                        <div class="channel-icon linkedin">
                            <i class="fab fa-linkedin-in"></i>
                        </div>
                        <span>LinkedIn</span>
                    </label>
                </div>
            </div>
        </div>

        <!-- Additional Options -->
        <div class="form-section">
            <label for="altText" class="form-label">
                <i class="fas fa-universal-access me-2"></i>
                Alt Text
            </label>
            <input
                type="text"
                class="form-control"
                id="altText"
                placeholder="Describe your media for accessibility"
                bind:value={altText}
            />
        </div>

        <div class="form-section">
            <label for="campaign" class="form-label">
                <i class="fas fa-bullhorn me-2"></i>
                Campaign
            </label>
            <input
                type="text"
                class="form-control"
                id="campaign"
                placeholder="Campaign name"
                bind:value={campaign}
            />
        </div>

        <div class="form-section">
            <label for="tags" class="form-label">
                <i class="fas fa-hashtag me-2"></i>
                Tags
            </label>
            <input
                type="text"
                class="form-control"
                id="tags"
                placeholder="Enter comma-separated tags (e.g., #marketing, #social)"
                bind:value={tags}
            />
        </div>

        <div class="form-section">
            <label for="firstComment" class="form-label">
                <i class="fas fa-comment me-2"></i>
                First Comment <span class="optional">(Optional)</span>
            </label>
            <textarea
                class="form-control"
                id="firstComment"
                rows="2"
                placeholder="This will be posted as the first comment on supported platforms"
                bind:value={firstComment}
            ></textarea>
        </div>

        <!-- Schedule Section -->
        <div class="form-section schedule-section">
            <label for="scheduleDate" class="form-label">
                <i class="fas fa-clock me-2"></i>
                Schedule Date & Time
            </label>
            <input
                type="datetime-local"
                class="form-control datetime-input"
                id="scheduleDate"
                bind:value={scheduleDate}
            />
        </div>

        <!-- Submit Button -->
        <div class="form-actions">
            <button
                type="submit"
                class="btn btn-primary btn-schedule"
                disabled={isSubmitting}
            >
                {#if isSubmitting}
                    <div class="spinner-border spinner-border-sm me-2" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    Scheduling...
                {:else}
                    <i class="fas fa-calendar-plus me-2"></i>
                    Schedule Post
                {/if}
            </button>
        </div>
    </form>
</div>

<style>
    .create-post-form {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .form-header {
        padding: 2rem 2rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
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
    }

    .form-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .form-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .post-form {
        padding: 2rem;
    }

    .form-section {
        margin-bottom: 2rem;
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }

    .form-label {
        display: flex;
        align-items: center;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
    }

    .form-label i {
        color: #667eea;
    }

    .optional {
        color: #9ca3af;
        font-weight: 400;
        font-size: 0.85rem;
    }

    .content-wrapper {
        position: relative;
    }

    .content-textarea {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        resize: vertical;
        min-height: 120px;
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

    .channels-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
    }

    .channel-item {
        position: relative;
    }

    .channel-item input[type="checkbox"] {
        position: absolute;
        opacity: 0;
        width: 100%;
        height: 100%;
        cursor: pointer;
        z-index: 2;
    }

    .channel-label {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.75rem;
        padding: 1.5rem 1rem;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }

    .channel-item input:checked + .channel-label {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }

    .channel-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }

    .channel-icon.facebook {
        background: #1877f2;
    }

    .channel-icon.instagram {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    }

    .channel-icon.x {
        background: #000000;
    }

    .channel-icon.linkedin {
        background: #0077b5;
    }

    .form-control {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }

    .form-control:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
        background: rgba(255, 255, 255, 0.95);
    }

    .datetime-input {
        font-family: 'Inter', sans-serif;
    }

    .schedule-section {
        background: rgba(102, 126, 234, 0.02);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .form-actions {
        text-align: center;
        padding-top: 1rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }

    .btn-schedule {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        width: 100%;
    }

    .btn-schedule:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        color: white;
    }

    .btn-schedule:disabled {
        opacity: 0.7;
        transform: none;
        cursor: not-allowed;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .form-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            text-align: center;
        }

        .post-form {
            padding: 1.5rem 1rem;
        }

        .form-row {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .channels-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .channel-label {
            padding: 1rem 0.5rem;
        }

        .btn-schedule {
            width: 100%;
            padding: 0.875rem 1.5rem;
        }
    }
</style>
