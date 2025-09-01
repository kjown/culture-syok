<script>
    import { onMount } from 'svelte';
    
    // Define the idea type
    /** @typedef {{
        id: number,
        image: string,
        title: string,
        description: string,
        status: string,
        createdDate: string,
        assignee: string,
        platform: string,
        notes: string,
        content?: string
    }} Idea */

    /** @type {Idea[]} */
    export let initialIdeas = [];
    
    /** @type {Idea[]} */
    let ideas = [];
    
    let activeTab = "Ideas";
    let tabs = ["Ideas", "To Do", "In Review", "Approved"];
    let link = "";
    let date = "";
    let time = "";
    let reminder = "";

    // Initialize ideas from props
    onMount(() => {
        ideas = [...initialIdeas];
    });

    // API functions
    /**
     * @param {Partial<Idea>} idea
     */
    async function saveIdeaToAPI(idea) {
        try {
            const response = await fetch('/api/collaborate/cards', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(idea)
            });
            
            if (response.ok) {
                const savedIdea = await response.json();
                return savedIdea;
            } else {
                throw new Error('Failed to save idea');
            }
        } catch (error) {
            console.error('Error saving idea:', error);
            throw error;
        }
    }

    /**
     * @param {Idea} idea
     */
    async function updateIdeaInAPI(idea) {
        try {
            const response = await fetch('/api/collaborate/cards', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(idea)
            });
            
            if (response.ok) {
                const updatedIdea = await response.json();
                return updatedIdea;
            } else {
                throw new Error('Failed to update idea');
            }
        } catch (error) {
            console.error('Error updating idea:', error);
            throw error;
        }
    }

    /**
     * @param {number} ideaId
     */
    async function deleteIdeaFromAPI(ideaId) {
        try {
            const response = await fetch('/api/collaborate/cards', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id: ideaId })
            });
            
            if (response.ok) {
                return true;
            } else {
                throw new Error('Failed to delete idea');
            }
        } catch (error) {
            console.error('Error deleting idea:', error);
            throw error;
        }
    }

    // Modal states
    let showViewModal = false;
    let showEditModal = false;
    let showAddModal = false;
    /** @type {Idea | null} */
    let selectedIdea = null;
    /** @type {Partial<Idea>} */
    let editingIdea = {};
    /** @type {Partial<Idea>} */
    let newIdea = {
        title: "",
        description: "",
        assignee: "",
        platform: "",
        image: "",
        notes: ""
    };

    // Image upload state
    let imageUploadMethod = "url"; // "url" or "file"
    /** @type {File | null} */
    let selectedImageFile = null;
    let imagePreview = "";

    // Functions for button actions
    /** @param {Idea} idea */
    function viewIdea(idea) {
        selectedIdea = idea;
        showViewModal = true;
    }

    /** @param {Idea} idea */
    function editIdea(idea) {
        selectedIdea = idea;
        editingIdea = { ...idea }; // Create a copy for editing
        showEditModal = true;
    }

    /** @param {number} ideaId */
    async function moveToNextPhase(ideaId) {
        const currentTabIndex = tabs.indexOf(activeTab);
        if (currentTabIndex < tabs.length - 1) {
            const nextStatus = tabs[currentTabIndex + 1];
            const ideaToUpdate = ideas.find(idea => idea.id === ideaId);
            
            if (ideaToUpdate) {
                try {
                    const updatedIdea = { ...ideaToUpdate, status: nextStatus };
                    await updateIdeaInAPI(updatedIdea);
                    
                    ideas = ideas.map(idea => 
                        idea.id === ideaId 
                            ? { ...idea, status: nextStatus }
                            : idea
                    );
                } catch (error) {
                    console.error('Failed to move idea to next phase:', error);
                    // Could show a toast notification here
                }
            }
        }
    }

    /** @param {number} ideaId */
    async function deleteIdea(ideaId) {
        if (confirm('Are you sure you want to delete this idea? This action cannot be undone.')) {
            try {
                await deleteIdeaFromAPI(ideaId);
                
                ideas = ideas.filter(idea => idea.id !== ideaId);
            } catch (error) {
                console.error('Failed to delete idea:', error);
                // Could show a toast notification here
            }
        }
    }

    function closeModal() {
        showViewModal = false;
        showEditModal = false;
        showAddModal = false;
        selectedIdea = null;
        editingIdea = {};
        newIdea = {
            title: "",
            description: "",
            assignee: "",
            platform: "",
            image: "",
            notes: ""
        };
        // Reset image upload state
        imageUploadMethod = "url";
        selectedImageFile = null;
        imagePreview = "";
    }

    async function saveEdit() {
        if (editingIdea.id) {
            try {
                /** @type {Idea} */
                const ideaToUpdate = {
                    id: editingIdea.id,
                    title: editingIdea.title || "",
                    description: editingIdea.description || "",
                    status: editingIdea.status || "Ideas",
                    createdDate: editingIdea.createdDate || new Date().toISOString().split('T')[0],
                    assignee: editingIdea.assignee || "Unassigned",
                    platform: editingIdea.platform || "Not specified",
                    image: editingIdea.image || "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop&crop=center",
                    notes: editingIdea.notes || "",
                    content: editingIdea.content || ""
                };
                
                await updateIdeaInAPI(ideaToUpdate);
                
                ideas = ideas.map(idea => 
                    idea.id === editingIdea.id 
                        ? { ...idea, ...ideaToUpdate }
                        : idea
                );
                closeModal();
            } catch (error) {
                console.error('Failed to save edit:', error);
                // Could show a toast notification here
            }
        }
    }

    function addNewIdea() {
        showAddModal = true;
    }

    async function saveNewIdea() {
        if (newIdea.title && newIdea.description) {
            // Use the appropriate image source
            let finalImageUrl = "";
            if (imageUploadMethod === "file" && imagePreview) {
                finalImageUrl = imagePreview; // Use the preview URL for the uploaded file
            } else if (imageUploadMethod === "url" && newIdea.image) {
                finalImageUrl = newIdea.image;
            } else {
                finalImageUrl = "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=300&h=200&fit=crop&crop=center";
            }
            
            /** @type {Partial<Idea>} */
            const ideaToAdd = {
                title: newIdea.title || "",
                description: newIdea.description || "",
                status: "Ideas",
                assignee: newIdea.assignee || "Unassigned",
                platform: newIdea.platform || "Not specified",
                image: finalImageUrl,
                notes: newIdea.notes || ""
            };
            
            try {
                const savedIdea = await saveIdeaToAPI(ideaToAdd);
                ideas = [...ideas, savedIdea];
                closeModal();
            } catch (error) {
                console.error('Failed to save new idea:', error);
                // Could show a toast notification here
            }
        }
    }

    // Handle escape key for modals
    /** @param {KeyboardEvent} event */
    function handleKeydown(event) {
        if (event.key === 'Escape' && (showViewModal || showEditModal || showAddModal)) {
            closeModal();
        }
    }

    // Handle image upload method change
    /** @param {string} method */
    function handleImageMethodChange(method) {
        imageUploadMethod = method;
        if (method === "url") {
            selectedImageFile = null;
            imagePreview = "";
        } else {
            newIdea.image = "";
        }
    }

    // Handle file upload
    /** @param {Event} event */
    function handleImageUpload(event) {
        const target = /** @type {HTMLInputElement} */ (event.target);
        if (target && target.files && target.files.length > 0) {
            const file = target.files[0];
            if (file) {
                selectedImageFile = file;
                
                // Create preview URL
                const reader = new FileReader();
                reader.onload = (e) => {
                    const result = e.target?.result;
                    if (typeof result === 'string') {
                        imagePreview = result;
                    }
                };
                reader.readAsDataURL(file);
            }
        }
    }

    // Filter ideas based on active tab
    $: filteredIdeas = ideas.filter(idea => idea.status === activeTab);
</script>

<svelte:window on:keydown={handleKeydown} />

<div class="collaborate-container">
    <!-- Enhanced Page Header -->
    <div class="page-header">
        <h1 class="page-title">
            <i class="fas fa-users me-3"></i>
            Team Collaboration
        </h1>
        <p class="page-subtitle">Collaborate with your team to plan, review, and approve content across all platforms</p>
    </div>

    <div class="collaboration-workspace">
        <!-- Main Content: Content Plan Board -->
        <div class="content-board">
            <div class="board-header">
                <div class="header-icon">
                    <i class="fas fa-project-diagram"></i>
                </div>
                <div>
                    <h3 class="board-title">Content Pipeline</h3>
                    <p class="board-subtitle">Track your content through every stage of production</p>
                </div>
            </div>

            <!-- Enhanced Tab Navigation -->
            <div class="tab-navigation">
                {#each tabs as tab}
                    <button
                        class="tab-btn"
                        class:active={activeTab === tab}
                        type="button"
                        on:click={() => (activeTab = tab)}
                    >
                        <div class="tab-content">
                            <span class="tab-label">{tab}</span>
                            <span class="tab-count">({ideas.filter(idea => idea.status === tab).length})</span>
                        </div>
                        {#if tab === "Ideas"}
                            <i class="fas fa-lightbulb tab-icon"></i>
                        {:else if tab === "To Do"}
                            <i class="fas fa-list-check tab-icon"></i>
                        {:else if tab === "In Review"}
                            <i class="fas fa-eye tab-icon"></i>
                        {:else if tab === "Approved"}
                            <i class="fas fa-check-circle tab-icon"></i>
                        {/if}
                    </button>
                {/each}
            </div>

            <!-- Tab Content -->
            <div class="tab-content-area">
                {#if filteredIdeas.length > 0}
                    <div class="ideas-grid">
                        {#each filteredIdeas as idea, index}
                            <div class="idea-card">
                                <div class="card-image">
                                    <img
                                        src={idea.image}
                                        alt={idea.title}
                                        class="idea-image"
                                    />
                                    <div class="image-overlay">
                                        <button class="overlay-btn view-btn" on:click={() => viewIdea(idea)}>
                                            <i class="fas fa-eye"></i>
                                        </button>
                                        <button class="overlay-btn edit-btn" on:click={() => editIdea(idea)}>
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        {#if activeTab !== "Approved"}
                                            <button class="overlay-btn move-btn" on:click={() => moveToNextPhase(idea.id)}>
                                                <i class="fas fa-arrow-right"></i>
                                            </button>
                                        {/if}
                                        <button class="overlay-btn delete-btn" on:click={() => deleteIdea(idea.id)}>
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                                <div class="card-content">
                                    <h6 class="idea-title">{idea.title}</h6>
                                    <p class="idea-description">{idea.description}</p>
                                    <div class="idea-meta">
                                        <span class="status-badge {idea.status.toLowerCase().replace(' ', '-')}">
                                            {idea.status}
                                        </span>
                                        <span class="date-badge">
                                            <i class="fas fa-clock"></i>
                                            {new Date(idea.createdDate).toLocaleDateString()}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                    
                    <!-- Add Button below ideas grid for Ideas tab -->
                    {#if activeTab === "Ideas"}
                        <div class="add-btn-container">
                            <button class="add-ideas-btn" on:click={addNewIdea}>
                                <i class="fas fa-plus"></i>
                                <span>Add New Idea</span>
                            </button>
                        </div>
                    {/if}
                {:else}
                    <div class="empty-state">
                        <div class="empty-icon">
                            {#if activeTab === "Ideas"}
                                <i class="fas fa-lightbulb"></i>
                            {:else if activeTab === "To Do"}
                                <i class="fas fa-tasks"></i>
                            {:else if activeTab === "In Review"}
                                <i class="fas fa-search"></i>
                            {:else}
                                <i class="fas fa-check-circle"></i>
                            {/if}
                        </div>
                        <h4 class="empty-title">No content in {activeTab.toLowerCase()}</h4>
                        <p class="empty-description">
                            {#if activeTab === "Ideas"}
                                Start by adding new content ideas to your pipeline.
                            {:else if activeTab === "To Do"}
                                Move ideas here when they're ready to be developed.
                            {:else if activeTab === "In Review"}
                                Content awaiting review will appear here.
                            {:else}
                                Approved content ready for publishing will be shown here.
                            {/if}
                        </p>
                        {#if activeTab === "Ideas"}
                            <button class="empty-action-btn" on:click={addNewIdea}>
                                <i class="fas fa-plus"></i>
                                Add New Content
                            </button>
                        {/if}
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<!-- View Modal -->
{#if showViewModal && selectedIdea}
    <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
    <div 
        class="modal-backdrop" 
        role="dialog" 
        aria-modal="true"
        on:click={closeModal}
    >
        <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
        <div 
            class="modal-content" 
            role="document"
            on:click|stopPropagation
        >
            <div class="modal-header">
                <h3 class="modal-title">
                    <i class="fas fa-eye"></i>
                    View Content Idea
                </h3>
                <button class="modal-close" on:click={closeModal}>
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="idea-image-container">
                    <img src={selectedIdea.image} alt={selectedIdea.title} class="modal-image" />
                </div>
                <div class="idea-details">
                    <div class="detail-group">
                        <span class="detail-label">Title:</span>
                        <p>{selectedIdea.title}</p>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Description:</span>
                        <p>{selectedIdea.description}</p>
                    </div>
                    {#if selectedIdea.content}
                        <div class="detail-group">
                            <span class="detail-label">Full Content Plan:</span>
                            <div class="content-preview">{@html selectedIdea.content.replace(/\n/g, '<br>')}</div>
                        </div>
                    {/if}
                    <div class="detail-row">
                        <div class="detail-group">
                            <span class="detail-label">Status:</span>
                            <span class="status-badge {selectedIdea.status.toLowerCase().replace(' ', '-')}">{selectedIdea.status}</span>
                        </div>
                        <div class="detail-group">
                            <span class="detail-label">Created:</span>
                            <p>{new Date(selectedIdea.createdDate).toLocaleDateString()}</p>
                        </div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-group">
                            <span class="detail-label">Assignee:</span>
                            <p>{selectedIdea.assignee}</p>
                        </div>
                        <div class="detail-group">
                            <span class="detail-label">Platform:</span>
                            <p>{selectedIdea.platform}</p>
                        </div>
                    </div>
                    <div class="detail-group">
                        <span class="detail-label">Notes:</span>
                        <p>{selectedIdea.notes}</p>
                    </div>
                </div>
                
                <!-- Action buttons in view modal -->
                <div class="modal-actions">
                    <button class="btn-edit" on:click={() => { closeModal(); if(selectedIdea) editIdea(selectedIdea); }}>
                        <i class="fas fa-edit"></i>
                        Edit
                    </button>
                    {#if selectedIdea.status !== "Approved"}
                        <button class="btn-move" on:click={() => { if(selectedIdea) moveToNextPhase(selectedIdea.id); closeModal(); }}>
                            <i class="fas fa-arrow-right"></i>
                            Move to Next
                        </button>
                    {/if}
                    <button class="btn-delete" on:click={() => { if(selectedIdea) deleteIdea(selectedIdea.id); closeModal(); }}>
                        <i class="fas fa-trash"></i>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}

<!-- Edit Modal -->
{#if showEditModal && editingIdea}
    <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
    <div 
        class="modal-backdrop" 
        role="dialog" 
        aria-modal="true"
        on:click={closeModal}
    >
        <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
        <div 
            class="modal-content" 
            role="document"
            on:click|stopPropagation
        >
            <div class="modal-header">
                <h3 class="modal-title">
                    <i class="fas fa-edit"></i>
                    Edit Content Idea
                </h3>
                <button class="modal-close" on:click={closeModal}>
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="edit-form">
                    <div class="form-group">
                        <label for="edit-title">Title:</label>
                        <input 
                            id="edit-title"
                            type="text" 
                            bind:value={editingIdea.title} 
                            class="form-input"
                        />
                    </div>
                    <div class="form-group">
                        <label for="edit-description">Description:</label>
                        <textarea 
                            id="edit-description"
                            bind:value={editingIdea.description} 
                            class="form-textarea"
                            rows="3"
                        ></textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="edit-assignee">Assignee:</label>
                            <input 
                                id="edit-assignee"
                                type="text" 
                                bind:value={editingIdea.assignee} 
                                class="form-input"
                            />
                        </div>
                        <div class="form-group">
                            <label for="edit-platform">Platform:</label>
                            <input 
                                id="edit-platform"
                                type="text" 
                                bind:value={editingIdea.platform} 
                                class="form-input"
                            />
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="edit-image">Image URL:</label>
                        <input 
                            id="edit-image"
                            type="url" 
                            bind:value={editingIdea.image} 
                            class="form-input"
                        />
                    </div>
                    <div class="form-group">
                        <label for="edit-notes">Notes:</label>
                        <textarea 
                            id="edit-notes"
                            bind:value={editingIdea.notes} 
                            class="form-textarea"
                            rows="3"
                        ></textarea>
                    </div>
                    <div class="form-actions">
                        <button class="btn-cancel" on:click={closeModal}>Cancel</button>
                        <button class="btn-save" on:click={saveEdit}>Save Changes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<!-- Add New Content Modal -->
{#if showAddModal}
    <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
    <div 
        class="modal-backdrop" 
        role="dialog" 
        aria-modal="true"
        on:click={closeModal}
    >
        <!-- svelte-ignore a11y-click-events-have-key-events a11y-no-static-element-interactions -->
        <div 
            class="modal-content" 
            role="document"
            on:click|stopPropagation
        >
            <div class="modal-header">
                <h3 class="modal-title">
                    <i class="fas fa-plus"></i>
                    Add New Content Idea
                </h3>
                <button class="modal-close" on:click={closeModal}>
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div class="edit-form">
                    <div class="form-group">
                        <label for="new-title">Title: <span class="required">*</span></label>
                        <input 
                            id="new-title"
                            type="text" 
                            bind:value={newIdea.title} 
                            class="form-input"
                            placeholder="Enter content idea title"
                            required
                        />
                    </div>
                    <div class="form-group">
                        <label for="new-description">Description: <span class="required">*</span></label>
                        <textarea 
                            id="new-description"
                            bind:value={newIdea.description} 
                            class="form-textarea"
                            rows="3"
                            placeholder="Describe your content idea"
                            required
                        ></textarea>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="new-assignee">Assignee:</label>
                            <input 
                                id="new-assignee"
                                type="text" 
                                bind:value={newIdea.assignee} 
                                class="form-input"
                                placeholder="Who will work on this?"
                            />
                        </div>
                        <div class="form-group">
                            <label for="new-platform">Platform:</label>
                            <input 
                                id="new-platform"
                                type="text" 
                                bind:value={newIdea.platform} 
                                class="form-input"
                                placeholder="Instagram, Facebook, etc."
                            />
                        </div>
                    </div>
                    <div class="form-group">
                        <fieldset class="image-fieldset">
                            <legend class="form-label">Image:</legend>
                        
                        <!-- Image upload method selection -->
                        <div class="image-method-tabs">
                            <button 
                                type="button"
                                class="method-tab"
                                class:active={imageUploadMethod === "url"}
                                on:click={() => handleImageMethodChange("url")}
                            >
                                <i class="fas fa-link"></i>
                                URL
                            </button>
                            <button 
                                type="button"
                                class="method-tab"
                                class:active={imageUploadMethod === "file"}
                                on:click={() => handleImageMethodChange("file")}
                            >
                                <i class="fas fa-upload"></i>
                                Upload
                            </button>
                        </div>

                        {#if imageUploadMethod === "url"}
                            <input 
                                id="new-image"
                                type="url" 
                                bind:value={newIdea.image} 
                                class="form-input"
                                placeholder="https://example.com/image.jpg"
                            />
                        {:else}
                            <div class="file-upload-area">
                                <input 
                                    id="new-image-file"
                                    type="file"
                                    accept="image/*"
                                    on:change={handleImageUpload}
                                    class="file-input"
                                />
                                <label for="new-image-file" class="file-upload-label">
                                    <i class="fas fa-cloud-upload-alt"></i>
                                    <span>Choose an image file</span>
                                    <small>JPG, PNG, GIF up to 5MB</small>
                                </label>
                                {#if selectedImageFile}
                                    <div class="file-info">
                                        <i class="fas fa-file-image"></i>
                                        <span>{selectedImageFile.name}</span>
                                    </div>
                                {/if}
                            </div>
                        {/if}

                        <!-- Image preview -->
                        {#if (imageUploadMethod === "url" && newIdea.image) || (imageUploadMethod === "file" && imagePreview)}
                            <div class="image-preview">
                                <img 
                                    src={imageUploadMethod === "url" ? newIdea.image : imagePreview} 
                                    alt="Preview" 
                                    class="preview-image"
                                />
                            </div>
                        {/if}
                        </fieldset>
                    </div>
                    <div class="form-group">
                        <label for="new-notes">Notes:</label>
                        <textarea 
                            id="new-notes"
                            bind:value={newIdea.notes} 
                            class="form-textarea"
                            rows="3"
                            placeholder="Additional notes or requirements"
                        ></textarea>
                    </div>
                    <div class="form-actions">
                        <button class="btn-cancel" on:click={closeModal}>Cancel</button>
                        <button 
                            class="btn-save" 
                            on:click={saveNewIdea}
                            disabled={!newIdea.title || !newIdea.description}
                        >
                            Add to Ideas
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
{/if}

<style>
    .collaborate-container {
        padding: 2rem 0;
        max-width: 1400px;
        margin: 0 auto;
    }

    /* Page Header */
    .page-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem 0;
        position: relative;
    }

    .page-title {
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .page-title i {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .page-subtitle {
        color: #718096;
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Collaboration Workspace */
    .collaboration-workspace {
        display: grid;
        gap: 2rem;
    }

    .content-board {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        overflow: hidden;
    }

    .board-header {
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

    .board-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .board-subtitle {
        margin: 0;
        color: #718096;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Tab Navigation */
    .tab-navigation {
        display: flex;
        gap: 0.5rem;
        margin: 2rem;
        margin-bottom: 0;
        background: rgba(102, 126, 234, 0.03);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }

    .tab-btn {
        flex: 1;
        background: transparent;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .tab-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .tab-btn:hover::before {
        opacity: 1;
    }

    .tab-btn.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transform: translateY(-1px);
    }

    .tab-btn.active .tab-content {
        color: white;
    }

    .tab-btn.active .tab-icon {
        color: white;
    }

    .tab-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        z-index: 2;
        color: #4a5568;
        font-weight: 600;
    }

    .tab-label {
        font-size: 0.95rem;
    }

    .tab-count {
        font-size: 0.8rem;
        opacity: 0.8;
    }

    .tab-icon {
        color: #667eea;
        font-size: 1.1rem;
        transition: color 0.3s ease;
    }

    /* Content Area */
    .tab-content-area {
        padding: 2rem;
        min-height: 400px;
    }

    .ideas-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }

    .idea-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
    }

    .idea-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .card-image {
        position: relative;
        height: 200px;
        overflow: hidden;
    }

    .idea-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .idea-card:hover .idea-image {
        transform: scale(1.05);
    }

    .image-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .idea-card:hover .image-overlay {
        opacity: 1;
    }

    .overlay-btn {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        color: #667eea;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 1rem;
    }

    .overlay-btn:hover {
        background: white;
        transform: scale(1.1);
    }

    .overlay-btn.delete-btn {
        color: #e53e3e;
    }

    .overlay-btn.delete-btn:hover {
        background: #fed7d7;
        color: #c53030;
    }

    .card-content {
        padding: 1.5rem;
    }

    .idea-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }

    .idea-description {
        color: #718096;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .idea-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }

    .status-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
    }

    .status-badge.ideas {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }

    .status-badge.to-do {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    }

    .status-badge.in-review {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    }

    .status-badge.approved {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }

    .date-badge {
        color: #9ca3af;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #718096;
    }

    .empty-icon {
        width: 80px;
        height: 80px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem;
        font-size: 2rem;
        color: #667eea;
    }

    .empty-title {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 0.75rem;
    }

    .empty-description {
        color: #718096;
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 2rem;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    }

    .empty-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 0.875rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .empty-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* Add Button Container */
    .add-btn-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(102, 126, 234, 0.1);
    }

    .add-ideas-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-size: 0.95rem;
    }

    .add-ideas-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .add-ideas-btn i {
        font-size: 1.1rem;
    }

    /* Required field indicator */
    .required {
        color: #e53e3e;
        font-weight: 700;
    }

    /* Fieldset styles */
    .image-fieldset {
        border: none;
        padding: 0;
        margin: 0;
    }

    .image-fieldset legend {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        padding: 0;
    }

    /* Disabled button styles */
    .btn-save:disabled {
        background: rgba(108, 117, 125, 0.3) !important;
        color: rgba(108, 117, 125, 0.7) !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Responsive design */
    @media (max-width: 1200px) {
        .collaborate-container {
            padding: 1.5rem 1rem;
        }
    }

    @media (max-width: 768px) {
        .page-title {
            font-size: 2rem;
            flex-direction: column;
            gap: 0.5rem;
        }

        .page-subtitle {
            font-size: 1rem;
        }

        .page-header {
            margin-bottom: 2rem;
            padding: 1.5rem 0;
        }

        .board-header {
            padding: 1.5rem 1rem 1rem;
            flex-direction: column;
            text-align: center;
        }

        .tab-navigation {
            margin: 1.5rem 1rem 0;
            flex-direction: column;
            gap: 0.5rem;
        }

        .tab-btn {
            padding: 0.875rem 1rem;
        }

        .tab-content-area {
            padding: 1.5rem 1rem;
        }

        .ideas-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }

        .empty-state {
            padding: 2rem 1rem;
        }

        .empty-icon {
            width: 60px;
            height: 60px;
            font-size: 1.5rem;
        }

        .empty-title {
            font-size: 1.1rem;
        }

        .empty-description {
            font-size: 0.9rem;
        }

        .add-btn-container {
            margin-top: 1.5rem;
            padding-top: 1rem;
        }

        .add-ideas-btn {
            padding: 0.875rem 1.5rem;
            font-size: 0.9rem;
        }
    }

    /* Modal Styles */
    .modal-backdrop {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        padding: 1rem;
        padding-top: 2rem;
    }

    .modal-content {
        background: white;
        border-radius: 20px;
        max-width: 90vw;
        width: 100%;
        max-width: 600px;
        max-height: 85vh;
        overflow-y: auto;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 2rem auto;
        position: relative;
    }

    .modal-header {
        padding: 1.5rem 2rem;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 20px 20px 0 0;
        position: sticky;
        top: 0;
        z-index: 10;
    }

    .modal-title {
        margin: 0;
        color: #2d3748;
        font-weight: 700;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .modal-title i {
        color: #667eea;
    }

    .modal-close {
        background: none;
        border: none;
        color: #718096;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 50%;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
    }

    .modal-close:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }

    .modal-body {
        padding: 1.5rem 2rem 2rem;
        max-height: calc(85vh - 120px);
        overflow-y: auto;
    }

    .idea-image-container {
        margin-bottom: 1.5rem;
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid rgba(102, 126, 234, 0.1);
    }

    .modal-image {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }

    .idea-details {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .detail-group {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }

    .detail-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .detail-group .detail-label {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
    }

    .detail-group p {
        margin: 0;
        color: #718096;
        line-height: 1.4;
    }

    .content-preview {
        background: rgba(102, 126, 234, 0.05);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        color: #4a5568;
        line-height: 1.6;
        max-height: 300px;
        overflow-y: auto;
        white-space: pre-wrap;
    }

    .modal-actions {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        flex-wrap: wrap;
    }

    .btn-edit,
    .btn-move,
    .btn-delete {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
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

    .btn-move {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }

    .btn-move:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
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

    .edit-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        max-height: none;
    }

    .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .form-group label {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
    }

    .form-input,
    .form-textarea {
        padding: 0.75rem 1rem;
        border: 2px solid rgba(102, 126, 234, 0.1);
        border-radius: 10px;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        font-family: inherit;
    }

    .form-input:focus,
    .form-textarea:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    .form-textarea {
        resize: vertical;
        min-height: 80px;
    }

    .form-actions {
        display: flex;
        gap: 1rem;
        justify-content: flex-end;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }

    .btn-cancel,
    .btn-save {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }

    .btn-cancel {
        background: rgba(108, 117, 125, 0.1);
        color: #6c757d;
        border: 2px solid rgba(108, 117, 125, 0.2);
    }

    .btn-cancel:hover {
        background: rgba(108, 117, 125, 0.2);
        border-color: rgba(108, 117, 125, 0.3);
    }

    .btn-save {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .btn-save:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    /* Image Upload Styles */
    .image-method-tabs {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        background: rgba(102, 126, 234, 0.05);
        padding: 0.25rem;
        border-radius: 8px;
    }

    .method-tab {
        flex: 1;
        background: transparent;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        color: #4a5568;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .method-tab:hover {
        background: rgba(102, 126, 234, 0.1);
    }

    .method-tab.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .file-upload-area {
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .file-upload-area:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.02);
    }

    .file-input {
        display: none;
    }

    .file-upload-label {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
        color: #4a5568;
    }

    .file-upload-label i {
        font-size: 2rem;
        color: #667eea;
    }

    .file-upload-label span {
        font-weight: 600;
        font-size: 1rem;
    }

    .file-upload-label small {
        color: #718096;
        font-size: 0.875rem;
    }

    .file-info {
        margin-top: 1rem;
        padding: 0.75rem;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #667eea;
    }

    .file-info i {
        font-size: 1.2rem;
    }

    .image-preview {
        margin-top: 1rem;
        border-radius: 10px;
        overflow: hidden;
        border: 2px solid rgba(102, 126, 234, 0.1);
    }

    .preview-image {
        width: 100%;
        height: 150px;
        object-fit: cover;
    }

    /* Mobile Modal Styles */
    @media (max-width: 768px) {
        .modal-backdrop {
            padding: 0.5rem;
            align-items: flex-start;
            padding-top: 1rem;
        }

        .modal-content {
            max-height: 95vh;
            max-width: 95vw;
            margin: 0;
        }

        .modal-header {
            padding: 1rem 1.5rem;
        }

        .modal-title {
            font-size: 1.1rem;
        }

        .modal-body {
            padding: 1rem 1.5rem 1.5rem;
            max-height: calc(95vh - 100px);
        }

        .modal-image {
            height: 150px;
        }

        .detail-row,
        .form-row {
            grid-template-columns: 1fr;
        }

        .form-actions {
            flex-direction: column;
        }

        .modal-actions {
            flex-direction: column;
        }

        .btn-cancel,
        .btn-save,
        .btn-edit,
        .btn-move,
        .btn-delete {
            width: 100%;
        }

        .image-method-tabs {
            margin-bottom: 0.75rem;
        }

        .method-tab {
            padding: 0.625rem 0.75rem;
            font-size: 0.9rem;
        }

        .file-upload-area {
            padding: 1rem;
        }

        .file-upload-label i {
            font-size: 1.5rem;
        }

        .file-upload-label span {
            font-size: 0.9rem;
        }

        .file-upload-label small {
            font-size: 0.8rem;
        }

        .preview-image {
            height: 120px;
        }
    }
</style>
