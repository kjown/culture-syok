import { writable } from 'svelte/store';

/**
 * @typedef {Object} Toast
 * @property {symbol} id
 * @property {string} message
 * @property {string} [actionText]
 * @property {() => void} [actionCallback]
 * @property {() => void} remove
 */

/** @type {import('svelte/store').Writable<Toast[]>} */
export const toasts = writable([]);

/**
 * Shows a toast notification.
 * @param {string} message The message to display.
 * @param {string} [actionText] Optional text for an action button (e.g., "View").
 * @param {() => void} [actionCallback] Optional function to run when the action is clicked.
 * @param {number} [timeout=5000] Duration in ms to show the toast.
 */
export function showToast(message, actionText, actionCallback, timeout = 5000) {
    const id = Symbol();

    const newToast = {
        id,
        message,
        actionText,
        actionCallback,
        remove: () => removeToast(id)
    };

    toasts.update((all) => [newToast, ...all]);

    setTimeout(() => removeToast(id), timeout);
}

/**
 * Removes a toast notification by its ID.
 * @param {symbol} id The unique ID of the toast to remove.
 */
function removeToast(id) {
    toasts.update((all) => all.filter((t) => t.id !== id));
}