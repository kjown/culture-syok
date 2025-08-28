// File: src/routes/api/media/upload/+server.js

import { json } from '@sveltejs/kit';
import { v2 as cloudinary } from 'cloudinary';
import { CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET } from '$env/static/private';

// Configure the Cloudinary SDK with your secret credentials.
// This is done on the server and is never exposed to the user's browser.
cloudinary.config({
    cloud_name: CLOUDINARY_CLOUD_NAME,
    api_key: CLOUDINARY_API_KEY,
    api_secret: CLOUDINARY_API_SECRET,
    secure: true
});

/**
 * Handles POST requests to upload a media file.
 * @type {import('./$types').RequestHandler}
 */
export async function POST({ request }) {
    try {
        // Get the form data from the incoming request.
        const formData = await request.formData();
        
        // Get the file from the form data. 'media' is the key we'll use on the frontend.
        const file = formData.get('media');

        if (!file) {
            return json({ success: false, error: 'No file was provided.' }, { status: 400 });
        }

        // To upload a file stream, we need to convert it to a buffer first.
        if (file instanceof Blob) {
            const arrayBuffer = await file.arrayBuffer();
            var buffer = Buffer.from(arrayBuffer);
        } else {
            return json({ success: false, error: 'Invalid file type.' }, { status: 400 });
        }

        // Use a Promise to handle the stream upload to Cloudinary.
        const uploadResult = await new Promise((resolve, reject) => {
            cloudinary.uploader.upload_stream(
                {
                    // Optionally, you can add upload settings here.
                    // For example, to store files in a specific folder:
                    folder: 'trendspotter_uploads'
                },
                (error, result) => {
                    if (error) {
                        return reject(error);
                    }
                    return resolve(result);
                }
            ).end(buffer);
        });

        // If the upload is successful, Cloudinary returns a result object.
        // We extract the secure URL.
        const secureUrl = uploadResult.secure_url;

        return json({ success: true, url: secureUrl });

    } catch (error) {
        console.error("Error during Cloudinary upload:", error);
        return json({ success: false, error: 'Upload failed. Please try again.' }, { status: 500 });
    }
}