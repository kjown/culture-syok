import { redirect } from '@sveltejs/kit';
import { google } from 'googleapis';

import { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ORIGIN } from '$env/static/private';

/**
 * This function runs when a user clicks a link to this endpoint
 * Its only job is to generate a unique Google login URL and send the user there.
 */
export async function GET() {
    // Create a new OAuth2 client with the app's credentials
    const oauth2Client = new google.auth.OAuth2(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        `${ORIGIN}/api/auth/callback`
    );

    // Define the permission to request from the user
    const scopes = [
        'https://www.googleapis.com/auth/calendar.events',
        'https://www.googleapis.com/auth/calendar.readonly'
    ];

    const url = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: scopes
    });

    throw redirect(302, url);
}