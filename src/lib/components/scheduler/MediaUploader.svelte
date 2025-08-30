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

<div class="media-uploader">
    {#if isLoading}
        <div class="upload-loading">
            <div class="loading-animation">
                <div class="loading-icon">
                    <i class="fas fa-cloud-upload-alt"></i>
                </div>
                <div class="loading-text">
                    <h6>Uploading your media...</h6>
                    <p>Please wait while we process your file</p>
                </div>
            </div>
        </div>
    {:else if uploadedImageUrl}
        <div class="uploaded-media">
            <div class="media-preview">
                <img
                    src={uploadedImageUrl}
                    alt="Uploaded preview"
                    class="preview-image"
                />
                <div class="media-overlay">
                    <button
                        on:click={removeImage}
                        class="btn-remove"
                        title="Remove media"
                    >
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="media-info">
                <div class="media-success">
                    <i class="fas fa-check-circle"></i>
                    <span>Media uploaded successfully</span>
                </div>
            </div>
        </div>
    {:else}
        <label for="file-upload" class="upload-area">
            <div class="upload-content">
                <div class="upload-icon">
                    <i class="fas fa-cloud-upload-alt"></i>
                </div>
                <div class="upload-text">
                    <h6>Drop your files here</h6>
                    <p>or <strong>click to browse</strong></p>
                    <small>Supports images and videos up to 10MB</small>
                </div>
            </div>
        </label>
        <input
            type="file"
            id="file-upload"
            class="file-input"
            accept="image/*,video/*"
            on:change={handleFileSelect}
        />
    {/if}

    {#if errorMessage}
        <div class="error-message">
            <i class="fas fa-exclamation-triangle"></i>
            <span>{errorMessage}</span>
        </div>
    {/if}
</div>

<style>
    .media-uploader {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        overflow: hidden;
    }

    .upload-area {
        display: block;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        border-radius: 15px;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
        border: 2px dashed #cbd5e0;
        position: relative;
        overflow: hidden;
    }

    .upload-area::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .upload-area:hover::before {
        opacity: 1;
    }

    .upload-area:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
    }

    .upload-content {
        position: relative;
        z-index: 1;
    }

    .upload-icon {
        font-size: 2.5rem;
        color: #667eea;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .upload-area:hover .upload-icon {
        transform: scale(1.1);
        color: #764ba2;
    }

    .upload-text h6 {
        margin: 0 0 0.5rem;
        color: #2d3748;
        font-weight: 600;
        font-size: 1.1rem;
    }

    .upload-text p {
        margin: 0 0 0.5rem;
        color: #718096;
        font-size: 0.95rem;
    }

    .upload-text strong {
        color: #667eea;
        font-weight: 600;
    }

    .upload-text small {
        color: #9ca3af;
        font-size: 0.8rem;
    }

    .file-input {
        display: none;
    }

    .upload-loading {
        padding: 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }

    .loading-animation {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .loading-icon {
        font-size: 2.5rem;
        color: #667eea;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.7;
            transform: scale(1.05);
        }
    }

    .loading-text h6 {
        margin: 0;
        color: #2d3748;
        font-weight: 600;
    }

    .loading-text p {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
    }

    .uploaded-media {
        padding: 1rem;
    }

    .media-preview {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .preview-image {
        width: 100%;
        height: auto;
        max-height: 300px;
        object-fit: cover;
        display: block;
    }

    .media-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: flex-start;
        justify-content: flex-end;
        padding: 1rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .media-preview:hover .media-overlay {
        opacity: 1;
    }

    .btn-remove {
        background: rgba(239, 68, 68, 0.9);
        border: none;
        color: white;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.9rem;
    }

    .btn-remove:hover {
        background: #dc2626;
        transform: scale(1.1);
    }

    .media-info {
        text-align: center;
    }

    .media-success {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #10b981;
        font-weight: 500;
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
        background: rgba(16, 185, 129, 0.1);
        border-radius: 20px;
    }

    .error-message {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
        padding: 1rem;
        border-radius: 0 0 15px 15px;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .upload-area {
            padding: 1.5rem 1rem;
        }

        .upload-icon {
            font-size: 2rem;
        }

        .upload-text h6 {
            font-size: 1rem;
        }

        .upload-text p {
            font-size: 0.85rem;
        }

        .loading-icon {
            font-size: 2rem;
        }
    }
</style>
