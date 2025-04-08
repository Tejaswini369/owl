import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, List, Optional
from fetch_server import FetchServer
from web_server import WebServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServer:
    """MCP Server for handling web operations."""
    
    def __init__(self, port: int = 9010):
        """Initialize the MCP server.
        
        Args:
            port: The port to listen on
        """
        self.port = port
        self.running = False
        self.server = None
        self.web_server = WebServer()
        
    async def start(self):
        """Start the MCP server."""
        if self.running:
            logger.warning("MCP server is already running")
            return
            
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, 'localhost', self.port
            )
            self.running = True
            logger.info(f"MCP server started on port {self.port}")
            
            async with self.server:
                await self.server.serve_forever()
        except Exception as e:
            logger.error(f"Error starting MCP server: {str(e)}", exc_info=True)
            self.running = False
            
    async def stop(self):
        """Stop the MCP server."""
        if not self.running:
            logger.warning("MCP server is not running")
            return
            
        try:
            self.server.close()
            await self.server.wait_closed()
            self.running = False
            logger.info("MCP server stopped")
        except Exception as e:
            logger.error(f"Error stopping MCP server: {str(e)}", exc_info=True)
            
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a connection to the MCP server.
        
        Args:
            reader: The stream reader
            writer: The stream writer
        """
        try:
            # Read the request length first (4 bytes)
            length_bytes = await reader.readexactly(4)
            request_length = int.from_bytes(length_bytes, byteorder='big')
            
            # Read the request
            data = await reader.readexactly(request_length)
            if not data:
                return
                
            # Parse the request
            request = json.loads(data.decode('utf-8'))
            logger.info(f"Received request: {request}")
            
            # Process the request
            response = await self.process_request(request)
            
            # Ensure proper JSON encoding
            response_json = json.dumps(response, ensure_ascii=False)
            response_bytes = response_json.encode('utf-8')
            
            # Send the response length first (4 bytes)
            writer.write(len(response_bytes).to_bytes(4, byteorder='big'))
            # Send the response
            writer.write(response_bytes)
            await writer.drain()
            
        except Exception as e:
            logger.error(f"Error handling connection: {str(e)}", exc_info=True)
            # Send error response
            error_response = {
                "error": str(e),
                "status": "error"
            }
            error_json = json.dumps(error_response, ensure_ascii=False)
            error_bytes = error_json.encode('utf-8')
            writer.write(len(error_bytes).to_bytes(4, byteorder='big'))
            writer.write(error_bytes)
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
            
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP request.
        
        Args:
            request: The request to process
            
        Returns:
            The response to the request
        """
        try:
            # Extract the operation from the request
            operation = request.get("operation")
            if not operation:
                return {
                    "error": "Operation is required",
                    "status": "error"
                }
                
            # Process the operation
            if operation == "search":
                return await self.web_server.search(
                    query=request.get("query", ""),
                    limit=request.get("limit", 10)
                )
            elif operation == "extract":
                return await self.web_server.extract(
                    url=request.get("url", "")
                )
            elif operation == "summarize":
                return await self.web_server.summarize(
                    content=request.get("content", ""),
                    length=request.get("length")
                )
            elif operation == "fetch_news":
                return await self.web_server.fetch_news(
                    query=request.get("query", ""),
                    sources=request.get("sources"),
                    limit=request.get("limit", 10)
                )
            elif operation == "filter_news":
                return await self.web_server.filter_news(
                    articles=request.get("articles", []),
                    keyword=request.get("keyword"),
                    start_date=request.get("start_date"),
                    end_date=request.get("end_date"),
                    limit=request.get("limit")
                )
            else:
                return {
                    "error": f"Unknown operation: {operation}",
                    "status": "error"
                }
                
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "error"
            }
            
    async def close(self):
        """Close the server."""
        await self.web_server.close()
        
async def main():
    """Main function."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get the port from command line arguments
    port = 9010
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid port: {sys.argv[1]}")
            return
            
    # Create and start the MCP server
    server = MCPServer(port)
    await server.start()
    
if __name__ == "__main__":
    asyncio.run(main()) 