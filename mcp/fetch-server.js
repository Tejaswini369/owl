
// fetch server startup script
const http = require('http');
const port = 3000;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    
    // Handle different endpoints
    if (req.url.startsWith('/fetch')) {
        // Simulate fetching data
        const data = {
            results: [
                { title: 'Sample News 1', source: 'Source 1', url: 'https://example.com/1', summary: 'This is a sample news summary 1' },
                { title: 'Sample News 2', source: 'Source 2', url: 'https://example.com/2', summary: 'This is a sample news summary 2' }
            ]
        };
        res.end(JSON.stringify(data));
    } else if (req.url.startsWith('/scrape')) {
        // Simulate web scraping
        const data = {
            content: 'This is a sample webpage content.',
            title: 'Sample Webpage',
            links: ['https://example.com/1', 'https://example.com/2']
        };
        res.end(JSON.stringify(data));
    } else if (req.url.startsWith('/execute')) {
        // Simulate command execution
        const data = {
            output: 'Command executed successfully',
            exitCode: 0
        };
        res.end(JSON.stringify(data));
    } else {
        // Default response
        const data = { message: 'fetch server is running' };
        res.end(JSON.stringify(data));
    }
});

server.listen(port, () => {
    console.log(`fetch server running on port ${port}`);
});
