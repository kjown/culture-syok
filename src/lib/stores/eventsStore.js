import { writable } from 'svelte/store';

/**
 * @typedef {Object} CalendarEvent
 * @property {string} id
 * @property {string} title
 * @property {string} start
 */

/** @type {import('svelte/store').Writable<CalendarEvent[]>} */
export const events = writable([]);