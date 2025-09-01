import { json } from '@sveltejs/kit';

// Define the Idea type
/** @typedef {{
    id: number,
    image: string,
    title: string,
    description: string,
    status: string,
    createdDate: string,
    assignee: string,
    platform: string,
    notes: string,
    content?: string
}} Idea */

// In-memory storage for demonstration (in a real app, use a database)
// Ideas array starts empty - all ideas come from generated content or user input
/** @type {Idea[]} */
let ideas = [];

let nextId = 1;

/** @type {import('./$types').RequestHandler} */
export async function GET() {
    return json(ideas);
}

/** @type {import('./$types').RequestHandler} */
export async function POST({ request }) {
    try {
        const data = await request.json();
        
        // Create new idea with generated ID and current date
        const newIdea = {
            id: nextId++,
            title: data.title || 'Untitled',
            content: data.content || '',
            description: data.description || data.content?.substring(0, 100) + '...' || '',
            status: data.status || 'Ideas',
            createdDate: new Date().toISOString().split('T')[0],
            assignee: data.assignee || 'Unassigned',
            platform: data.platform || 'Multiple Platforms',
            image: data.image || 'https://static.vecteezy.com/system/resources/thumbnails/007/446/072/small_2x/light-bulb-concept-and-ideas-hand-drawn-illustration-vector.jpg',
            notes: data.notes || 'Generated from AI content plan'
        };
        
        ideas.push(newIdea);
        
        return json(newIdea, { status: 201 });
    } catch (error) {
        console.error('Error creating idea:', error);
        return json({ error: 'Failed to create idea' }, { status: 500 });
    }
}

/** @type {import('./$types').RequestHandler} */
export async function PUT({ request }) {
    try {
        const data = await request.json();
        const { id, ...updateData } = data;
        
        const ideaIndex = ideas.findIndex(idea => idea.id === id);
        
        if (ideaIndex === -1) {
            return json({ error: 'Idea not found' }, { status: 404 });
        }
        
        ideas[ideaIndex] = { ...ideas[ideaIndex], ...updateData };
        
        return json(ideas[ideaIndex]);
    } catch (error) {
        console.error('Error updating idea:', error);
        return json({ error: 'Failed to update idea' }, { status: 500 });
    }
}

/** @type {import('./$types').RequestHandler} */
export async function DELETE({ request }) {
    try {
        const { id } = await request.json();
        
        const ideaIndex = ideas.findIndex(idea => idea.id === id);
        
        if (ideaIndex === -1) {
            return json({ error: 'Idea not found' }, { status: 404 });
        }
        
        ideas.splice(ideaIndex, 1);
        
        return json({ success: true });
    } catch (error) {
        console.error('Error deleting idea:', error);
        return json({ error: 'Failed to delete idea' }, { status: 500 });
    }
}
