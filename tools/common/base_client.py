import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from owl import OWL

class BaseClient(ABC):
    """Base class for all tool clients."""
    
    def __init__(self):
        """Initialize the base client."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.owl = None
    
    async def initialize(self) -> None:
        """Initialize the client and any necessary resources."""
        self.owl = OWL()
        await self.owl.initialize()
    
    async def cleanup(self) -> None:
        """Clean up any resources used by the client."""
        if self.owl:
            await self.owl.cleanup()
    
    def _handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle errors in a consistent way across all clients."""
        error_msg = f"Error in {context}: {str(error)}" if context else str(error)
        self.logger.error(error_msg)
        return {
            'status': 'error',
            'error': error_msg
        }
    
    def _validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate that a response has the required fields."""
        return (
            isinstance(response, dict) and
            'status' in response and
            response['status'] in ['success', 'error']
        ) 