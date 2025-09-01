export async function load({ fetch }) {
    try {
        const response = await fetch('/api/collaborate/cards');
        const ideas = await response.json();
        
        return {
            ideas
        };
    } catch (error) {
        console.error('Error loading ideas:', error);
        return {
            ideas: []
        };
    }
}