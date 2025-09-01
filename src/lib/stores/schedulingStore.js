import { writable } from 'svelte/store';

/**
 * @typedef {Object} ScheduledPostData
 * @property {string} caption
 * @property {string} campaign
 * @property {string[]} tags
 */

/**
 * A writable store to temporarily hold approved content data when navigating
 * from the collaboration page to the scheduler page.
 * It is cleared immediately after the data is read by the scheduler form
 * to prevent re-populating on a page refresh.
 * @type {import('svelte/store').Writable<ScheduledPostData | null>}
 */
export const postToSchedule = writable(null);
