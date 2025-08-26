import { error, json } from '@sveltejs/kit';
import { getGoogleCalendarClient } from '$lib/utils/google.server';

/**
 * PUT: Update an existing scheduled post
 *  @param {{ request: Request, cookies: import('@sveltejs/kit').Cookies, params: { eventId: string } }} param
 */
export async function PUT({ request, cookies, params }) {
    const calendar = getGoogleCalendarClient(cookies.get('g_tokens') ?? '');
    if (!calendar) {
        return json({ error: 'User not authenticated.' }, { status: 401 });
    }

    const { eventId } = params;
    const eventData = await request.json();

    try {
        const response = await calendar.events.update({
            calendarId: 'primary',
            eventId: eventId,
            requestBody: eventData,
        });
        return json({ success:  true, event: response.data });
    } catch (error) {
        console.error('Error updating event:', error);
        return json({ error: 'Failed to update event.' }, { status: 500 });
    }
}

/**
 * DELETE: Delete a scheduled post
 * @param {{ request: Request, cookies: import('@sveltejs/kit').Cookies, params: { eventId: string } }} param
 */
export async function DELETE({ cookies, params }) {
    const calendar = getGoogleCalendarClient(cookies.get('g_tokens') ?? '');
    if (!calendar) {
        return json({ error: 'User not authenticated' }, { status: 401 });
    }

    const { eventId } = params;

    try {
        await calendar.events.delete({
            calendarId: 'primary',
            eventId: eventId,
        });
        return json({ success: true });
    } catch (error) {
        console.error('Error deleting event:', error);
        return json({ error: 'Failed to delete event.' }, { status: 500 });
    }
}

