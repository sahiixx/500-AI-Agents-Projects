"""
Base tool class for Dubai Real Estate workflow tools.
This provides a minimal BaseTool implementation compatible with CrewAI.
"""

from typing import Any
from pydantic import BaseModel, Field


class BaseTool(BaseModel):
    """
    Base class for all custom tools in the Dubai Real Estate workflow.

    This provides a simple interface for creating tools that can be used
    with CrewAI agents.
    """

    name: str = Field(default="", description="The name of the tool")
    description: str = Field(default="", description="A description of what the tool does")

    class Config:
        arbitrary_types_allowed = True

    def _run(self, *args, **kwargs) -> Any:
        """
        The main execution method for the tool.
        Should be overridden by subclasses.

        Returns:
            The result of the tool execution
        """
        raise NotImplementedError("Subclasses must implement _run method")

    def run(self, *args, **kwargs) -> Any:
        """
        Public method to execute the tool.
        Calls the _run method internally.

        Returns:
            The result of the tool execution
        """
        return self._run(*args, **kwargs)
