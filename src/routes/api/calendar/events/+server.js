import { json } from '@sveltejs/kit';
import { getGoogleCalendarClient } from '$lib/utils/google.server';

/**
 * GET: Fetch all scheduled posts (events) from the user's calendar
 *
 * @param {Object} param
 * @param {import('@sveltejs/kit').Cookies} param.cookies
*/
export async function GET({ cookies }) {
    const calendar = getGoogleCalendarClient(cookies.get('g_tokens') ?? '');
    if (!calendar) {
        return json({ error: 'User not authenticated.'}, { status: 401 });
    }

    try {
        const response = await calendar.events.list({
            calendarId: 'primary',
            timeMin: new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString(),
            maxResults: 250,
            singleEvents: true,
            orderBy: 'startTime',
        });

        return json(response.data.items);
    } catch (error) {
        console.error('Error fetching calendar events', error);
        return json({ error: 'Failed to fetch calendar events.' }, { status: 500});
    }
}

/**
 * POST: Create a new scheduled post (event) on the user's calendar.
 * 
 * @param {{ request: Request, cookies: import('@sveltejs/kit').Cookies }} param
*/
export async function POST({ request, cookies }) {
    const calendar = getGoogleCalendarClient(cookies.get('g_tokens') ?? '');
    if (!calendar) {
        return json({ error: 'User not authenticated.'}, { status: 401 });
    }

    const eventData = await request.json();

    try {
        const response = await calendar.events.insert({
            calendarId: 'primary',
            requestBody: {
                summary: eventData.summary,
                description: eventData.description,
                start: {
                    dateTime: eventData.start,
                },
                end: {
                    dateTime: eventData.end,
                },
            },
        });

        return json({ success: true, event: response.data });
    } catch (error) {
        console.error('Error creating calendar event:', error);
        return json({ error: 'Failed to create calendar event.'}, { status: 500 });
    }
}