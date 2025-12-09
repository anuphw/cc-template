# Claude Code Project Template

## Project Overview
This is a task-agnostic template for effective problem-solving with Claude Code, optimized for context window usage, parallel execution, and session continuity.

## Commands & Quick Start
- `uv run python` - Python execution
- `/compact` - Compress conversation history
- `/context` - Check token usage and memory status
- `/clear` - Hard reset when context drifts
- `--continue` - Resume most recent session
- `--fork-session` - Create new session branch

## Workflow Standards

### 1. Problem Understanding Phase
- **Requirement Analysis**: Break down the problem into core components
- **Context Discovery**: Understand existing codebase and constraints
- **Success Criteria**: Define clear, measurable outcomes
- **Risk Assessment**: Identify potential blockers and dependencies

### 2. Solution Architecture
- **Task Decomposition**: Create independent sub-problems for parallel execution
- **Agent Assignment**: Match specialized agents to appropriate tasks
- **Execution Strategy**: Plan parallel vs serial execution paths
- **Verification Plan**: Define testing and validation approaches

### 3. Implementation Guidelines
- **Context Preservation**: Log decisions and rationale in session-log.md
- **Progress Tracking**: Maintain active todo lists with real-time updates
- **Quality Gates**: Run linting, type-checking, and tests before completion
- **Documentation**: Update context files for future sessions

## Agent Specializations

### Core Agents (`.claude/agents/`)
- **codebase-locator**: Finds files and components (WHERE code lives)
- **codebase-analyzer**: Analyzes implementation details (HOW code works)
- **research-synthesizer**: Connects patterns and creates insights
- **web-research-specialist**: External documentation and best practices

### Original Template Agents (`.claude/skills/`)
- **problem-solver**: Systematic problem decomposition
- **context-manager**: Session continuity and thought process logging
- **parallel-coordinator**: Multi-agent orchestration

### Research Command
Use for comprehensive codebase investigation:
```bash
Task(subagent_type="research", description="Research [TOPIC]",
     prompt="Research [DETAILED_QUESTION]")
```

## Memory Management
- **session-log.md** - Thought process and decision logging
- **context-state.md** - Current project understanding and state
- **CLAUDE.local.md** - Local environment specifics (gitignored)

## Integration Points
- Python: PyTorch, Flask, FastAPI, Jupyter notebooks
- Testing: pytest, unittest, coverage analysis
- Code Quality: ruff, mypy, pre-commit hooks
- Version Control: Git workflow with automated commit patterns

## Utility Scripts (`hack/`)
- **understand_project_structure.sh**: Comprehensive project analysis for agents
- **project_metadata.sh**: Generate metadata for research documentation