import { google } from '$lib/utils/google.server.js';

/**
 * Fetches approved ideas from the collaborate API.
 * @param {Request} request - The request object to get the origin
 * @returns {Promise<Array<any>>}
 */
async function fetchApprovedIdeas(request) {
    try {
        // Get the origin from the request to make an internal API call
        const url = new URL(request.url);
        const apiUrl = `${url.origin}/api/collaborate/cards`;
        
        const response = await fetch(apiUrl);
        if (response.ok) {
            const ideas = await response.json();
            
            // Filter for approved ideas only and format them for the scheduler
            return ideas.filter((/** @type {any} */ idea) => idea.status === 'Approved').map((/** @type {any} */ idea) => ({
                id: idea.id,
                title: idea.title,
                description: idea.description,
                status: idea.status,
                platform: idea.platform,
                tags: idea.platform ? idea.platform.split(',').map((/** @type {string} */ tag) => tag.trim()) : []
            }));
        } else {
            console.error('Failed to fetch ideas from API');
            return [];
        }
    } catch (error) {
        console.error('Error fetching approved ideas:', error);
        return [];
    }
}

/**
 * Loads calendar events and approved ideas for the scheduler page.
 * @param {{ locals: { user?: { accessToken: string } }, request: Request }} param0
 */
export async function load({ locals, request }) {
    // Fetch approved ideas from the collaborate API
    const approvedIdeas = await fetchApprovedIdeas(request);

    if (!locals.user) {
        return {
            events: [],
            approvedIdeas: approvedIdeas // Return ideas even if not logged in
        };
    }

    try {
        const calendar = google.calendar({
            version: 'v3',
            auth: locals.user.accessToken
        });

        const response = await calendar.events.list({
            calendarId: 'primary',
            timeMin: new Date().toISOString(),
            maxResults: 50,
            singleEvents: true,
            orderBy: 'startTime'
        });

        return {
            events: response.data.items || [],
            approvedIdeas: approvedIdeas
        };
    } catch (error) {
        console.error('Error fetching calendar events:', error);
        return {
            events: [],
            approvedIdeas: approvedIdeas // Still return ideas on error
        };
    }
}