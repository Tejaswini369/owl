import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubServer:
    """MCP GitHub Server for GitHub-related operations."""
    
    def __init__(self, port: int = 8003):
        """Initialize the GitHub server.
        
        Args:
            port: The port to listen on
        """
        self.port = port
        self.running = False
        self.server = None
        self.github_token = os.getenv("GITHUB_TOKEN")
        
    async def start(self):
        """Start the GitHub server."""
        if self.running:
            logger.warning("GitHub server is already running")
            return
            
        try:
            self.server = await asyncio.start_server(
                self.handle_connection, 'localhost', self.port
            )
            self.running = True
            logger.info(f"GitHub server started on port {self.port}")
            
            async with self.server:
                await self.server.serve_forever()
        except Exception as e:
            logger.error(f"Error starting GitHub server: {str(e)}", exc_info=True)
            self.running = False
            
    async def stop(self):
        """Stop the GitHub server."""
        if not self.running:
            logger.warning("GitHub server is not running")
            return
            
        try:
            self.server.close()
            await self.server.wait_closed()
            self.running = False
            logger.info("GitHub server stopped")
        except Exception as e:
            logger.error(f"Error stopping GitHub server: {str(e)}", exc_info=True)
            
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle a connection to the GitHub server.
        
        Args:
            reader: The stream reader
            writer: The stream writer
        """
        try:
            # Read the request
            data = await reader.read(1024)
            if not data:
                return
                
            # Parse the request
            request = json.loads(data.decode())
            logger.info(f"Received request: {request}")
            
            # Process the request
            response = await self.process_request(request)
            
            # Send the response
            writer.write(json.dumps(response).encode())
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
        """Process a GitHub request.
        
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
            if operation == "search_repos":
                return await self.search_repos(request)
            elif operation == "get_repo":
                return await self.get_repo(request)
            elif operation == "get_file":
                return await self.get_file(request)
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
            
    async def search_repos(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Search for GitHub repositories.
        
        Args:
            request: The search request
            
        Returns:
            The search results
        """
        try:
            # Extract the query from the request
            query = request.get("query")
            if not query:
                return {
                    "error": "Query is required",
                    "status": "error"
                }
                
            # Extract optional parameters
            sort = request.get("sort", "stars")
            order = request.get("order", "desc")
            limit = request.get("limit", 10)
            
            # Perform the search
            results = await self._search_repositories(query, sort, order, limit)
            
            # Return the results
            return {
                "results": results,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error searching repositories: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "error"
            }
            
    async def get_repo(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about a GitHub repository.
        
        Args:
            request: The get request
            
        Returns:
            The repository information
        """
        try:
            # Extract the owner and repo from the request
            owner = request.get("owner")
            repo = request.get("repo")
            if not owner or not repo:
                return {
                    "error": "Owner and repo are required",
                    "status": "error"
                }
                
            # Get the repository information
            repo_info = await self._get_repository(owner, repo)
            
            # Return the repository information
            return {
                "repository": repo_info,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error getting repository: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "error"
            }
            
    async def get_file(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get the content of a file in a GitHub repository.
        
        Args:
            request: The get request
            
        Returns:
            The file content
        """
        try:
            # Extract the owner, repo, path, and branch from the request
            owner = request.get("owner")
            repo = request.get("repo")
            path = request.get("path")
            branch = request.get("branch", "main")
            
            if not owner or not repo or not path:
                return {
                    "error": "Owner, repo, and path are required",
                    "status": "error"
                }
                
            # Get the file content
            content = await self._get_file_content(owner, repo, path, branch)
            
            # Return the file content
            return {
                "content": content,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error getting file: {str(e)}", exc_info=True)
            return {
                "error": str(e),
                "status": "error"
            }
            
    async def _search_repositories(self, query: str, sort: str = "stars", 
                                 order: str = "desc", limit: int = 10) -> List[Dict[str, Any]]:
        """Search for GitHub repositories.
        
        Args:
            query: The search query
            sort: The sort field (stars, forks, updated)
            order: The sort order (asc, desc)
            limit: The maximum number of results to return
            
        Returns:
            The search results
        """
        # This is a placeholder implementation
        # In a real implementation, you would use the GitHub API
        return [
            {
                "name": f"repo-{i}",
                "full_name": f"owner/repo-{i}",
                "description": f"Description for repo-{i}",
                "stars": i * 100,
                "forks": i * 10,
                "url": f"https://github.com/owner/repo-{i}"
            }
            for i in range(1, limit + 1)
        ]
        
    async def _get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get information about a GitHub repository.
        
        Args:
            owner: The repository owner
            repo: The repository name
            
        Returns:
            The repository information
        """
        # This is a placeholder implementation
        # In a real implementation, you would use the GitHub API
        return {
            "name": repo,
            "full_name": f"{owner}/{repo}",
            "description": f"Description for {owner}/{repo}",
            "stars": 100,
            "forks": 10,
            "url": f"https://github.com/{owner}/{repo}"
        }
        
    async def _get_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> str:
        """Get the content of a file in a GitHub repository.
        
        Args:
            owner: The repository owner
            repo: The repository name
            path: The file path
            branch: The branch name
            
        Returns:
            The file content
        """
        # This is a placeholder implementation
        # In a real implementation, you would use the GitHub API
        return f"Content of {path} in {owner}/{repo} on branch {branch}"

async def main():
    """Main function to run the GitHub server."""
    # Get the port from command line arguments or use default
    port = 8003
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error(f"Invalid port: {sys.argv[1]}")
            return
            
    # Create and start the GitHub server
    server = GitHubServer(port)
    await server.start()

if __name__ == "__main__":
    asyncio.run(main()) 