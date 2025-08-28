<!-- src/lib/components/scheduler/MediaUploader.svelte -->
<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let isLoading = false;
    /** @type {string|null} */
    let uploadedImageUrl = null;
    let errorMessage = "";

    /**
     * @param {Event} event
     */
    async function handleFileSelect(event) {
        const input = /** @type {HTMLInputElement|null} */ (event.target);
        if (!input || !input.files || input.files.length === 0) return;
        const file = input.files[0];

        isLoading = true;
        errorMessage = "";

        const formData = new FormData();
        formData.append("media", file); // 'media' must match the key on the backend.

        try {
            const response = await fetch("/api/media/upload", {
                method: "POST",
                body: formData,
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                throw new Error(result.error || "Failed to upload.");
            }

            uploadedImageUrl = result.url;
            // Notify the parent component that the upload is complete, sending the URL.
            dispatch("uploadComplete", uploadedImageUrl);
        } catch (/** @type {any} */ error) {
            errorMessage = error.message;
            console.error(error);
        } finally {
            isLoading = false;
        }
    }

    function removeImage() {
        uploadedImageUrl = null;
        // Notify the parent that the image has been removed.
        dispatch("uploadComplete", null);
    }
</script>

<div class="card bg-light p-3">
    {#if isLoading}
        <div
            class="d-flex justify-content-center align-items-center"
            style="height: 150px;"
        >
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span class="ms-2">Uploading...</span>
        </div>
    {:else if uploadedImageUrl}
        <div class="position-relative">
            <img
                src={uploadedImageUrl}
                alt="Uploaded preview"
                class="img-fluid rounded"
            />
            <button
                on:click={removeImage}
                class="btn btn-sm btn-danger position-absolute top-0 end-0 m-2"
            >
                &times; <!-- A simple 'X' icon -->
            </button>
        </div>
    {:else}
        <label
            for="file-upload"
            class="form-label text-center p-4 border-2 border-dashed rounded"
            style="cursor: pointer;"
        >
            Click to upload media
        </label>
        <input
            type="file"
            id="file-upload"
            class="d-none"
            accept="image/*,video/*"
            on:change={handleFileSelect}
        />
    {/if}

    {#if errorMessage}
        <div class="alert alert-danger mt-3">{errorMessage}</div>
    {/if}
</div>

<style>
    .border-dashed {
        border: 2px dashed #ccc;
    }
    .border-dashed:hover {
        border-color: #0d6efd;
        background-color: #f8f9fa;
    }
</style>
