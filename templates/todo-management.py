#!/usr/bin/env python3
"""
Task decomposition and tracking utilities for Claude Code workflows.
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Task:
    """Represents a single task in the execution plan."""
    id: str
    content: str
    active_form: str
    status: str = "pending"
    dependencies: List[str] = None
    estimated_duration: Optional[int] = None
    tags: List[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class TodoManager:
    """Manages task decomposition and tracking for complex projects."""

    def __init__(self, session_data_dir: str = "session-data"):
        self.session_data_dir = Path(session_data_dir)
        self.session_data_dir.mkdir(exist_ok=True)
        self.todos_file = self.session_data_dir / "todos.json"

    def generate_execution_plan(self, problem: str, context: str = "") -> Dict[str, Any]:
        """Generate a structured execution plan for a given problem."""

        # This is a template - in practice, this would use AI/ML to decompose tasks
        plan = {
            "problem": problem,
            "context": context,
            "created_at": datetime.now().isoformat(),
            "tasks": [],
            "parallel_groups": []
        }

        # Example decomposition logic (replace with actual AI-powered decomposition)
        if "authentication" in problem.lower():
            tasks = [
                Task("auth-1", "Design user authentication model", "Designing user authentication model", tags=["architecture", "auth"]),
                Task("auth-2", "Implement JWT token handling", "Implementing JWT token handling", tags=["implementation", "auth"]),
                Task("auth-3", "Create login/logout endpoints", "Creating login/logout endpoints", tags=["api", "auth"]),
                Task("auth-4", "Add authentication middleware", "Adding authentication middleware", tags=["middleware", "auth"]),
                Task("auth-5", "Write authentication tests", "Writing authentication tests", dependencies=["auth-1", "auth-2", "auth-3"], tags=["testing", "auth"])
            ]
        else:
            # Generic task decomposition
            tasks = [
                Task(str(uuid.uuid4()), f"Analyze requirements for: {problem}", f"Analyzing requirements for: {problem}", tags=["analysis"]),
                Task(str(uuid.uuid4()), f"Design solution architecture", f"Designing solution architecture", tags=["architecture"]),
                Task(str(uuid.uuid4()), f"Implement core functionality", f"Implementing core functionality", tags=["implementation"]),
                Task(str(uuid.uuid4()), f"Add comprehensive tests", f"Adding comprehensive tests", tags=["testing"]),
                Task(str(uuid.uuid4()), f"Review and optimize", f"Reviewing and optimizing", tags=["review"])
            ]

        plan["tasks"] = [self._task_to_dict(task) for task in tasks]
        plan["parallel_groups"] = self.identify_parallel_opportunities(tasks)

        return plan

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert Task object to dictionary."""
        return {
            "id": task.id,
            "content": task.content,
            "activeForm": task.active_form,
            "status": task.status,
            "dependencies": task.dependencies,
            "estimated_duration": task.estimated_duration,
            "tags": task.tags,
            "created_at": task.created_at
        }

    def get_claude_todo_format(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert tasks to Claude's TodoWrite format."""
        return [
            {
                "content": task["content"],
                "status": task["status"],
                "activeForm": task["activeForm"]
            }
            for task in tasks
        ]

    def identify_parallel_opportunities(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """Identify which tasks can be executed in parallel."""
        parallel_groups = {}
        stage = 0

        # Simple dependency-based grouping
        remaining_tasks = {task.id: task for task in tasks}
        completed_tasks = set()

        while remaining_tasks:
            current_stage = []
            for task_id, task in list(remaining_tasks.items()):
                if all(dep in completed_tasks for dep in task.dependencies):
                    current_stage.append(task_id)
                    completed_tasks.add(task_id)
                    del remaining_tasks[task_id]

            if current_stage:
                parallel_groups[f"stage_{stage}"] = current_stage
                stage += 1
            else:
                # Break circular dependencies
                if remaining_tasks:
                    task_id = next(iter(remaining_tasks.keys()))
                    current_stage.append(task_id)
                    completed_tasks.add(task_id)
                    del remaining_tasks[task_id]
                    parallel_groups[f"stage_{stage}"] = current_stage
                    stage += 1

        return parallel_groups

    def save_todos(self, tasks: List[Dict[str, Any]]):
        """Save current todo list to session data."""
        with open(self.todos_file, 'w') as f:
            json.dump(tasks, f, indent=2)

    def load_todos(self) -> List[Dict[str, Any]]:
        """Load todo list from session data."""
        if self.todos_file.exists():
            with open(self.todos_file, 'r') as f:
                return json.load(f)
        return []

    def update_task_status(self, task_id: str, status: str, log_entry: str = ""):
        """Update task status and log the change."""
        todos = self.load_todos()
        for task in todos:
            if task.get("id") == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                if log_entry:
                    if "log" not in task:
                        task["log"] = []
                    task["log"].append({
                        "timestamp": datetime.now().isoformat(),
                        "entry": log_entry
                    })
                break
        self.save_todos(todos)

if __name__ == "__main__":
    # Example usage
    manager = TodoManager()

    # Generate plan for authentication system
    plan = manager.generate_execution_plan(
        problem="Build user authentication system with JWT tokens",
        context="FastAPI backend with PostgreSQL database"
    )

    print("Execution Plan:")
    print(f"Problem: {plan['problem']}")
    print(f"Tasks: {len(plan['tasks'])}")
    print("\nParallel Groups:")
    for group, tasks in plan['parallel_groups'].items():
        print(f"  {group}: {tasks}")

    # Get Claude-compatible format
    claude_todos = manager.get_claude_todo_format(plan["tasks"])
    print(f"\nClaude Todo Format: {len(claude_todos)} items")