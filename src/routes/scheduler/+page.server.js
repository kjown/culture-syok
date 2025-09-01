import { google } from '$lib/utils/google.server.js';

/**
 * MOCK DATA: In a real application, this would come from your database.
 */
const allIdeas = [
    { id: 1, title: 'Raya Promotion', description: 'Special discounts for Hari Raya.', status: 'In Review', platform: 'Facebook, Instagram', tags: ['raya2025', 'sale'] },
    { id: 2, title: 'Merdeka Day Contest', description: 'Run a user-generated content contest for Merdeka.', status: 'Approved', platform: 'Instagram', tags: ['merdeka', 'contest', 'malaysia'] },
    { id: 3, title: 'Deepavali Greetings', description: 'A simple and elegant Deepavali greeting post.', status: 'Approved', platform: 'Facebook, Twitter', tags: ['deepavali', 'festival'] },
    { id: 4, title: 'New Year Campaign Kick-off', description: 'Teaser for the upcoming new year campaign.', status: 'To Do', platform: 'All', tags: ['newyear', 'campaign'] }
];

/**
 * Loads calendar events and approved ideas for the scheduler page.
 * @param {{ locals: { user?: { accessToken: string } } }} param0
 */
export async function load({ locals }) {
    // Filter the mock data to get only approved ideas
    const approvedIdeas = allIdeas.filter(idea => idea.status === 'Approved');

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