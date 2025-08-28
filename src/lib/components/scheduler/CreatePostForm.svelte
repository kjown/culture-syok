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
                <MediaUploader
                    bind:this={mediaUploaderRef}
                    on:uploadComplete={handleUploadComplete}
                />
            <div class="mb-3">
                <label class="form-label">Channels</label>
                <div>
                    <div class="form-check form-check-inline">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="facebook"
                            value="Facebook"
                            bind:group={channels}
                        />
                        <label class="form-check-label" for="facebook"
                            >Facebook</label
                        >
                    </div>
                    <div class="form-check form-check-inline">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="instagram"
                            value="Instagram"
                            bind:group={channels}
                        />
                        <label class="form-check-label" for="instagram"
                            >Instagram</label
                        >
                    </div>
                    <div class="form-check form-check-inline">
                        <input
                            class="form-check-input"
                            type="checkbox"
                            id="twitter"
                            value="Twitter"
                            bind:group={channels}
                        />
                        <label class="form-check-label" for="twitter"
                            >Twitter</label
                        >
                    </div>
                </div>
            </div>
            <div class="mb-3">
                <label for="altText" class="form-label"
                    >Alt Text for Media</label
                >
                <input
                    type="text"
                    class="form-control"
                    id="altText"
                    bind:value={altText}
                />
                <div class="form-text">
                    Describe your image for accessibility.
                </div>
            </div>
            <div class="mb-3">
                <label for="campaign" class="form-label">Campaign</label>
                <input
                    type="text"
                    class="form-control"
                    id="campaign"
                    bind:value={campaign}
                />
            </div>
            <div class="mb-3">
                <label for="tags" class="form-label">Tags</label>
                <input
                    type="text"
                    class="form-control"
                    id="tags"
                    bind:value={tags}
                />
                <div class="form-text">Enter comma-separated tags.</div>
            </div>
            <div class="mb-3">
                <label for="firstComment" class="form-label"
                    >Optional First Comment</label
                >
                <textarea
                    class="form-control"
                    id="firstComment"
                    rows="2"
                    bind:value={firstComment}
                ></textarea>
                <div class="form-text">
                    This will be posted as the first comment on supported
                    platforms.
                </div>
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
