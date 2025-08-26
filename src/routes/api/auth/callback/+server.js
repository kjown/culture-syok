import { redirect } from "@sveltejs/kit";
import { google } from "googleapis";
import { GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ORIGIN } from "$env/static/private";

/**
 * This function runs when Google redirects the user back to the app
 * @param {{ url: URL, cookies: import('@sveltejs/kit').Cookies }} param
 */
export async function GET({ url, cookies }) {
    // Get temporary 'code' that Google sends back in the URL
    const code = url.searchParams.get('code');

    if (!code) {
        throw redirect(302, '/');
    }

    const oauth2Client = new google.auth.OAuth2(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        `${ORIGIN}/api/auth/callback`
    );

    const { tokens } = await oauth2Client.getToken(code);

    // Securely store the tokens in a cookie
    // 'httpOnly: true' is a crucial security measure that prevents client-side Javascript from ever accessing this cookie
    cookies.set('g_tokens', JSON.stringify(tokens), {
        path: '/',
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        maxAge: 60 * 60 * 24 * 30
    });

    throw redirect(302, '/'); 
}