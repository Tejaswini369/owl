import asyncio
import json
import logging
import aiohttp
import base64
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FetchServer:
    """MCP Fetch Server for retrieving web content."""
    
    def __init__(self, port: int = 9001):
        """Initialize the fetch server.
        
        Args:
            port: The port to listen on
        """
        self.port = port
        self.running = False
        self.server = None
        
    async def start(self):
        """Start the fetch server."""
        if self.running:
            logger.warning("Fetch server is already running")
            return
            
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, 'localhost', self.port
            )
            self.running = True
            logger.info(f"Fetch server started on port {self.port}")
            
            async with self.server:
                await self.server.serve_forever()
        except Exception as e:
            logger.error(f"Error starting fetch server: {str(e)}", exc_info=True)
            self.running = False
            
    async def stop(self):
        """Stop the fetch server."""
        if not self.running:
            logger.warning("Fetch server is not running")
            return
            
        try:
            self.server.close()
            await self.server.wait_closed()
            self.running = False
            logger.info("Fetch server stopped")
        except Exception as e:
            logger.error(f"Error stopping fetch server: {str(e)}", exc_info=True)
            
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a connection to the fetch server.
        
        Args:
            reader: The stream reader
            writer: The stream writer
        """
        try:
            # Read the request
            data = await reader.read(4096)  # Increased buffer size
            if not data:
                return
                
            # Parse the request
            request = json.loads(data.decode())
            logger.info(f"Received request: {request}")
            
            # Process the request
            response = await self.process_request(request)
            
            # Ensure proper JSON encoding
            response_json = json.dumps(response, ensure_ascii=False)
            
            # Send the response
            writer.write(response_json.encode())
            await writer.drain()
            
        except Exception as e:
            logger.error(f"Error handling connection: {str(e)}", exc_info=True)
            # Send error response
            error_response = {
                "error": str(e),
                "status": "error"
            }
            writer.write(json.dumps(error_response).encode())
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
            
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a fetch request.
        
        Args:
            request: The request to process
            
        Returns:
            The response to the request
        """
        try:
            # Extract the URL from the request
            url = request.get("url")
            if not url:
                return {
                    "error": "URL is required",
                    "status": "error"
                }
                
            # Extract optional parameters
            params = request.get("params", {})
            
            # Fetch the content
            content = await self.fetch_content(url, params)
            
            # Encode the content
            try:
                # Try to encode as UTF-8 first
                content_bytes = content.encode('utf-8')
            except UnicodeEncodeError:
                # If that fails, use a more lenient encoding
                content_bytes = content.encode('utf-8', errors='replace')
                
            # Ensure proper base64 encoding with padding
            encoded_content = base64.b64encode(content_bytes).decode('ascii')
            
            # Return the response
            return {
                "content": encoded_content,
                "url": url,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "error"
            }
            
    async def fetch_content(self, url: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Fetch content from a URL.
        
        Args:
            url: The URL to fetch content from
            params: Optional parameters for the request
            
        Returns:
            The fetched content
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    return await response.text()
        except Exception as e:
            logger.error(f"Error fetching content: {str(e)}", exc_info=True)
            raise

async def main():
    """Main function to run the fetch server."""
    # Create and start the fetch server
    server = FetchServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main()) 