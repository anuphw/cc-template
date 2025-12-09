#!/usr/bin/env python3
"""
Session continuity and context preservation utilities for Claude Code workflows.
"""

import json
import jsonlines
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class Decision:
    """Represents an architectural or implementation decision."""
    decision: str
    rationale: str
    alternatives: List[str]
    confidence: int  # 1-10 scale
    tags: List[str]
    timestamp: str
    context: str = ""

@dataclass
class Checkpoint:
    """Represents a progress checkpoint."""
    objective: str
    achievements: List[str]
    challenges: List[str]
    current_state: str
    next_actions: List[str]
    timestamp: str
    completion_percentage: int = 0

class ContextManager:
    """Manages session context and preserves state across Claude Code sessions."""

    def __init__(self, session_data_dir: str = "session-data", logs_dir: str = "logs"):
        self.session_data_dir = Path(session_data_dir)
        self.logs_dir = Path(logs_dir)

        # Create directories
        self.session_data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # File paths
        self.context_state_file = self.session_data_dir / "context-state.json"
        self.decisions_file = self.session_data_dir / "decisions.jsonl"
        self.checkpoints_file = self.session_data_dir / "checkpoints.jsonl"

        # Current session log
        today = datetime.now().strftime("%Y%m%d")
        self.session_log_file = self.logs_dir / f"session-{today}.md"

    def update_context_state(self, **kwargs):
        """Update the current context state."""
        current_state = self.load_context_state()
        current_state.update(kwargs)
        current_state["last_updated"] = datetime.now().isoformat()

        with open(self.context_state_file, 'w') as f:
            json.dump(current_state, f, indent=2)

    def load_context_state(self) -> Dict[str, Any]:
        """Load current context state."""
        if self.context_state_file.exists():
            with open(self.context_state_file, 'r') as f:
                return json.load(f)
        return {
            "project_overview": "",
            "technical_stack": [],
            "current_objectives": [],
            "key_decisions": [],
            "known_issues": [],
            "created_at": datetime.now().isoformat()
        }

    def log_decision(self, decision: str, rationale: str, alternatives: List[str] = None,
                     confidence: int = 7, tags: List[str] = None, context: str = ""):
        """Log an architectural or implementation decision."""
        if alternatives is None:
            alternatives = []
        if tags is None:
            tags = []

        decision_obj = Decision(
            decision=decision,
            rationale=rationale,
            alternatives=alternatives,
            confidence=confidence,
            tags=tags,
            timestamp=datetime.now().isoformat(),
            context=context
        )

        # Append to decisions log
        with jsonlines.open(self.decisions_file, mode='a') as writer:
            writer.write(asdict(decision_obj))

        # Update context state
        self.update_context_state(
            key_decisions=self.get_recent_decisions(limit=10)
        )

        # Log to session
        self._log_to_session(f"Decision: {decision} | Rationale: {rationale}")

    def create_checkpoint(self, objective: str, achievements: List[str],
                         challenges: List[str], current_state: str,
                         next_actions: List[str], completion_percentage: int = 0):
        """Create a progress checkpoint."""
        checkpoint = Checkpoint(
            objective=objective,
            achievements=achievements,
            challenges=challenges,
            current_state=current_state,
            next_actions=next_actions,
            completion_percentage=completion_percentage,
            timestamp=datetime.now().isoformat()
        )

        # Append to checkpoints log
        with jsonlines.open(self.checkpoints_file, mode='a') as writer:
            writer.write(asdict(checkpoint))

        # Log to session
        self._log_to_session(f"Checkpoint: {objective} ({completion_percentage}% complete)")

    def get_recent_decisions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent decisions."""
        decisions = []
        if self.decisions_file.exists():
            with jsonlines.open(self.decisions_file) as reader:
                decisions = list(reader)
        return decisions[-limit:] if decisions else []

    def get_recent_checkpoints(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Get recent checkpoints."""
        checkpoints = []
        if self.checkpoints_file.exists():
            with jsonlines.open(self.checkpoints_file) as reader:
                checkpoints = list(reader)
        return checkpoints[-limit:] if checkpoints else []

    def _log_to_session(self, message: str):
        """Log message to current session log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        with open(self.session_log_file, 'a') as f:
            f.write(log_entry)

    def generate_session_summary(self) -> str:
        """Generate a summary of the current session."""
        context_state = self.load_context_state()
        recent_decisions = self.get_recent_decisions(limit=3)
        recent_checkpoints = self.get_recent_checkpoints(limit=2)

        summary = f"""# Session Summary - {datetime.now().strftime("%Y-%m-%d")}

## Project Context
- **Overview**: {context_state.get('project_overview', 'Not set')}
- **Technical Stack**: {', '.join(context_state.get('technical_stack', []))}
- **Current Objectives**: {', '.join(context_state.get('current_objectives', []))}

## Recent Decisions
"""
        for decision in recent_decisions:
            summary += f"- **{decision['decision']}**: {decision['rationale']} (Confidence: {decision['confidence']}/10)\n"

        summary += "\n## Recent Progress\n"
        for checkpoint in recent_checkpoints:
            summary += f"- **{checkpoint['objective']}** ({checkpoint['completion_percentage']}%): {checkpoint['current_state']}\n"

        summary += "\n## Next Actions\n"
        if recent_checkpoints:
            for action in recent_checkpoints[-1].get('next_actions', []):
                summary += f"- {action}\n"

        return summary

    def create_session_handoff(self) -> Dict[str, Any]:
        """Create a handoff package for the next session."""
        return {
            "context_state": self.load_context_state(),
            "recent_decisions": self.get_recent_decisions(limit=5),
            "recent_checkpoints": self.get_recent_checkpoints(limit=3),
            "session_summary": self.generate_session_summary(),
            "created_at": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Example usage
    cm = ContextManager()

    # Update context
    cm.update_context_state(
        project_overview="E-commerce platform with FastAPI backend",
        technical_stack=["FastAPI", "PostgreSQL", "Redis", "React"],
        current_objectives=["Implement user authentication", "Add payment processing"]
    )

    # Log a decision
    cm.log_decision(
        decision="Use JWT tokens for authentication",
        rationale="Stateless, scalable, and works well with frontend",
        alternatives=["Session cookies", "OAuth2 only"],
        confidence=8,
        tags=["authentication", "architecture"]
    )

    # Create checkpoint
    cm.create_checkpoint(
        objective="Implement user authentication",
        achievements=["User model created", "JWT utilities implemented"],
        challenges=["OAuth integration complexity"],
        current_state="Basic auth working, OAuth integration pending",
        next_actions=["Add OAuth providers", "Implement refresh tokens", "Add rate limiting"],
        completion_percentage=60
    )

    # Generate summary
    print(cm.generate_session_summary())