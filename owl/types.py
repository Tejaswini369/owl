"""
OWL types module.
This module contains custom type definitions used throughout the OWL package.
"""

from typing import Any, Callable, Dict, List, Optional, Union

class Tool:
    """A class representing a tool that can be used by an agent."""
    
    def __init__(
        self,
        name: str,
        description: str,
        func: Callable,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a Tool.
        
        Args:
            name: The name of the tool
            description: A description of what the tool does
            func: The function that implements the tool's functionality
            parameters: Optional dictionary describing the tool's parameters
        """
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters or {}
        
    def __call__(self, *args, **kwargs):
        """Call the tool's function with the given arguments."""
        return self.func(*args, **kwargs)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        } 