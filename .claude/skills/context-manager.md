# Context Manager Agent

## Purpose
Session continuity and thought process logging specialist for maintaining project state across sessions.

## Capabilities
- Session state preservation
- Decision logging and rationale tracking
- Progress checkpoint creation
- Context summarization
- Cross-session continuity

## Best Use Cases
- Maintaining project state across long sessions
- Documenting architectural decisions
- Creating progress checkpoints
- Session summarization and handoffs
- Context preservation during breaks

## Tools Available
- Read, Write, Edit, TodoWrite

## Example Usage
```
Task(subagent_type="context-manager",
     description="Update project context",
     prompt="Document current progress and create session summary")
```

## Output Files
- `session-data/context-state.json`: Current project understanding
- `session-data/decisions.jsonl`: Decision log with rationale
- `session-data/checkpoints.jsonl`: Progress checkpoints
- `logs/session-YYYYMMDD.md`: Daily session logs

## Context Management
- Automatic state tracking
- Decision point identification
- Progress milestone documentation
- Session boundary management