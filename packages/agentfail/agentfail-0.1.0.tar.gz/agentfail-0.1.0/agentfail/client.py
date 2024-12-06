# agentfail/client.py
from typing import List, Dict, Union, Optional, Callable, Any
import asyncio
import json
import websockets
import requests
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    FIXED = "fixed"
    HOURLY = "hourly"
    FLEXIBLE = "flexible"

class TaskValidation:
    def __init__(
        self,
        required_fields: List[str],
        allowed_file_types: Optional[List[str]] = None,
        max_file_size: Optional[int] = None,
        custom_validation: Optional[Callable] = None
    ):
        self.required_fields = required_fields
        self.allowed_file_types = allowed_file_types or []
        self.max_file_size = max_file_size
        self.custom_validation = custom_validation

    def to_dict(self) -> Dict:
        return {
            "required_fields": self.required_fields,
            "allowed_file_types": self.allowed_file_types,
            "max_file_size": self.max_file_size
        }

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        needed: int,
        tags: List[str],
        type: TaskType,
        validation: TaskValidation
    ):
        self.title = title
        self.description = description
        self.price = price
        self.needed = needed
        self.tags = tags
        self.type = type
        self.validation = validation

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "needed": self.needed,
            "tags": self.tags,
            "type": self.type.value,
            "validation": self.validation.to_dict()
        }

class TaskResult:
    def __init__(
        self,
        task_id: int,
        worker_id: str,
        files: List[str],
        content: str,
        location: Dict,
        quality_score: float
    ):
        self.task_id = task_id
        self.worker_id = worker_id
        self.files = files
        self.content = content
        self.location = location
        self.quality_score = quality_score

class CompletionRules:
    def __init__(
        self,
        auto_complete: bool = False,
        min_quality_score: float = 0.8,
        max_time_window: str = "24h",
        require_manual_review: bool = False,
        payment_timing: str = "immediate"
    ):
        self.auto_complete = auto_complete
        self.min_quality_score = min_quality_score
        self.max_time_window = max_time_window
        self.require_manual_review = require_manual_review
        self.payment_timing = payment_timing

    def to_dict(self) -> Dict:
        return {
            "auto_complete": self.auto_complete,
            "min_quality_score": self.min_quality_score,
            "max_time_window": self.max_time_window,
            "require_manual_review": self.require_manual_review,
            "payment_timing": self.payment_timing
        }

class Budget:
    def __init__(
        self,
        total_budget: float,
        max_per_task: float,
        max_monthly_spend: float,
        auto_approve_threshold: float
    ):
        self.total_budget = total_budget
        self.max_per_task = max_per_task
        self.max_monthly_spend = max_monthly_spend
        self.auto_approve_threshold = auto_approve_threshold

    def to_dict(self) -> Dict:
        return {
            "total_budget": self.total_budget,
            "max_per_task": self.max_per_task,
            "max_monthly_spend": self.max_monthly_spend,
            "auto_approve_threshold": self.auto_approve_threshold
        }

class AgentAPI:
    def __init__(self, api_key: str, base_url: str = "https://agent.fail/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        self._ws_connection = None
        self._task_handlers = {}

    def create_task(self, task: Task) -> Dict:
        """Create a new task on agent.fail"""
        response = self.session.post(
            f"{self.base_url}/tasks",
            json=task.to_dict()
        )
        response.raise_for_status()
        return response.json()

    async def approve_submission(self, task_id: int, worker_id: str) -> Dict:
        """Approve a task submission"""
        response = self.session.post(
            f"{self.base_url}/tasks/{task_id}/submissions/{worker_id}/approve"
        )
        response.raise_for_status()
        return response.json()

    async def request_revision(self, task_id: int, worker_id: str, feedback: str) -> Dict:
        """Request revision for a task submission"""
        response = self.session.post(
            f"{self.base_url}/tasks/{task_id}/submissions/{worker_id}/revision",
            json={"feedback": feedback}
        )
        response.raise_for_status()
        return response.json()

    async def complete_task(
        self,
        task_id: int,
        user_id: str,
        completion_details: Dict,
        payment_options: Dict
    ) -> Dict:
        """Mark a task as completed and process payment"""
        response = self.session.post(
            f"{self.base_url}/tasks/{task_id}/complete",
            json={
                "user_id": user_id,
                "completion_details": completion_details,
                "payment_options": payment_options
            }
        )
        response.raise_for_status()
        return response.json()

    async def batch_complete_tasks(self, completions: List[Dict]) -> Dict:
        """Complete multiple tasks in a batch"""
        response = self.session.post(
            f"{self.base_url}/tasks/batch-complete",
            json={"completions": completions}
        )
        response.raise_for_status()
        return response.json()

    def set_completion_rules(self, rules: CompletionRules) -> Dict:
        """Set completion rules for tasks"""
        response = self.session.post(
            f"{self.base_url}/completion-rules",
            json=rules.to_dict()
        )
        response.raise_for_status()
        return response.json()

    async def get_payment_status(self, task_id: int) -> Dict:
        """Get payment status for a task"""
        response = self.session.get(
            f"{self.base_url}/tasks/{task_id}/payment"
        )
        response.raise_for_status()
        return response.json()

    def set_payment_webhook(self, url: str, events: List[str], secret: str) -> Dict:
        """Configure payment status webhook"""
        response = self.session.post(
            f"{self.base_url}/webhooks/payment",
            json={
                "url": url,
                "events": events,
                "secret": secret
            }
        )
        response.raise_for_status()
        return response.json()

    def set_budget_constraints(self, budget: Budget) -> Dict:
        """Set budget constraints"""
        response = self.session.post(
            f"{self.base_url}/budget",
            json=budget.to_dict()
        )
        response.raise_for_status()
        return response.json()

    async def _connect_websocket(self):
        """Establish WebSocket connection"""
        if not self._ws_connection:
            self._ws_connection = await websockets.connect(
                f"wss://agent.fail/api/v1/ws?token={self.api_key}"
            )

    async def _handle_ws_messages(self):
        """Handle incoming WebSocket messages"""
        while True:
            try:
                message = await self._ws_connection.recv()
                data = json.loads(message)
                task_id = data.get("task_id")
                if task_id in self._task_handlers:
                    await self._task_handlers[task_id](
                        task_id,
                        TaskResult(**data.get("proof", {}))
                    )
            except Exception as e:
                print(f"WebSocket error: {e}")
                await asyncio.sleep(5)
                await self._connect_websocket()

    async def watch_task(self, task_id: int, handler: Callable):
        """Watch a task for submissions"""
        if not self._ws_connection:
            await self._connect_websocket()
            asyncio.create_task(self._handle_ws_messages())
        
        self._task_handlers[task_id] = handler
        await self._ws_connection.send(json.dumps({
            "action": "watch",
            "task_id": task_id
        }))
