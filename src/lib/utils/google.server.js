import { google } from 'googleapis';
import { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET } from '$env/static/private';

/**
 * Creates an authenticated Google Calendar API client
 * @param {string} tokensCookie - The raw 'g_tokens' cookie value
 * @returns {import('googleapis').calendar_v3.Calendar | null} - An authenticated client of null if tokens are invalid
 */

export function getGoogleCalendarClient(tokensCookie) {
    if (!tokensCookie) {
        return null;
    }

    try {
        const tokens = JSON.parse(tokensCookie);
        const oauth2Client = new google.auth.OAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET);
        oauth2Client.setCredentials(tokens);
        return google.calendar({ version: 'v3', auth: oauth2Client });
    } catch (error) {
        console.error("Failed to parse tokens or create client", error);
        return null;
    }
}