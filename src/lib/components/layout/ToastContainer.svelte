<script>
    import { toasts } from "$lib/stores/toastStore.js";
    import { fly } from "svelte/transition";

    /**
     * @param {{ actionCallback?: Function, remove: Function }} toast
     */
    function handleAction(toast) {
        if (toast.actionCallback) {
            toast.actionCallback();
        }
        toast.remove();
    }
</script>

<div class="toast-container">
    {#each $toasts as toast (toast.id)}
        <div
            class="toast-item"
            in:fly={{ y: 20, duration: 300 }}
            out:fly={{ y: 20, duration: 200 }}
        >
            <span class="toast-message">{toast.message}</span>
            {#if toast.actionText}
                <button
                    class="toast-action"
                    on:click={() => handleAction(toast)}
                >
                    {toast.actionText}
                </button>
            {/if}
            <button class="toast-close" on:click={toast.remove}>&times;</button>
        </div>
    {/each}
</div>

<style>
    .toast-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 9999;
    }

    .toast-item {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 12px 20px;
        background-color: #2d3748;
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        font-size: 0.95rem;
        min-width: 250px;
        max-width: 400px;
    }

    .toast-message {
        flex-grow: 1;
    }

    .toast-action {
        background: none;
        border: none;
        color: #818cf8;
        font-weight: 600;
        cursor: pointer;
        padding: 5px;
        margin: -5px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }

    .toast-action:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    .toast-close {
        background: none;
        border: none;
        color: #a0aec0;
        font-size: 1.5rem;
        line-height: 1;
        cursor: pointer;
        opacity: 0.7;
    }
    .toast-close:hover {
        opacity: 1;
    }
</style>
