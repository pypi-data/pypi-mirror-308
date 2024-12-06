"""
agent.fail Python Client

A Python library for AIs to create tasks and receive human-verified proof of completion 
through images, text, files, or any other form of evidence.
"""

from .client import (
    AgentAPI,
    Task,
    TaskType,
    TaskValidation,
    TaskResult,
    CompletionRules,
    Budget,
)

__version__ = "0.1.0"
__author__ = "aied"
__email__ = "admin@aied.uk"

# Make key classes available at package level
__all__ = [
    "AgentAPI",
    "Task",
    "TaskType",
    "TaskValidation",
    "TaskResult",
    "CompletionRules",
    "Budget",
]