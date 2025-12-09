# Claude Code Template (anuphw/cc-template)

A comprehensive, production-ready template for effective problem-solving with Claude Code, optimized for context window usage, parallel execution, and session continuity. This template provides a structured approach to complex software development tasks through specialized agents, automated workflows, and intelligent context management.

## 🚀 Quick Start

```bash
# Use this template
git clone https://github.com/anuphw/cc-template.git your-project-name
cd your-project-name

# Start a new Claude Code session
claude --continue  # Resume previous session
claude --fork-session  # Create new branch from previous session

# Check context status
/context

# Compress history when needed
/compact

# Hard reset if context drifts
/clear

# Python execution (as configured)
uv run python
```

## 📁 Template Structure

```
claude-code-template/
├── CLAUDE.md                      # Main project configuration
├── CLAUDE.local.md                # Local environment specifics (gitignored)
├── .claude/                       # Claude Code configuration
│   ├── agents/                    # Specialized research agents (NEW)
│   │   ├── codebase-analyzer.md   # Implementation analysis specialist
│   │   ├── codebase-locator.md    # File and component finder
│   │   ├── research-synthesizer.md # Pattern recognition and synthesis
│   │   └── web-research-specialist.md # External research specialist
│   ├── commands/                  # Structured workflow commands (NEW)
│   │   └── research.md            # Comprehensive research command
│   └── skills/                    # Original template agents
│       ├── problem-solver.md      # Problem decomposition specialist
│       ├── context-manager.md     # Session and context management
│       └── parallel-coordinator.md # Multi-agent orchestration
├── templates/                     # Python orchestration tools
│   ├── todo-management.py         # Task decomposition and tracking
│   ├── context-preservation.py    # Session continuity and logging
│   └── orchestrator.py           # Agent execution coordination
├── hack/                          # Utility scripts (NEW)
│   ├── understand_project_structure.sh # Project analysis for agents
│   ├── project_metadata.sh        # Metadata generation
│   └── README.md                  # Utility documentation
├── session-data/                  # Auto-generated session state
│   ├── todos.json                 # Current task list
│   ├── context-state.json         # Project understanding
│   ├── decisions.jsonl            # Decision log
│   └── checkpoints.jsonl          # Progress checkpoints
└── logs/                          # Execution and session logs
    ├── session-YYYYMMDD.md        # Daily session logs
    └── executions/                # Agent execution logs
```

## 🎯 Core Workflow

### 1. Problem Understanding Phase

```bash
# Start with problem decomposition
uv run python templates/todo-management.py

# Or use the problem-solver agent
Task(subagent_type="problem-solver", description="Analyze requirements",
     prompt="Break down this problem: [YOUR_PROBLEM]")
```

**Key Activities:**
- **Requirement Analysis**: Break down core components
- **Context Discovery**: Understand existing codebase
- **Success Criteria**: Define measurable outcomes
- **Risk Assessment**: Identify blockers and dependencies

### 2. Solution Architecture

```bash
# Generate execution plan
uv run python templates/orchestrator.py

# Update project context
uv run python -c "
from templates.context_preservation import ContextManager
cm = ContextManager()
cm.update_context_state(
    project_overview='Your project description',
    technical_stack=['FastAPI', 'PostgreSQL', 'React']
)
"
```

**Key Activities:**
- **Task Decomposition**: Create independent sub-problems
- **Agent Assignment**: Match specialized agents to tasks
- **Execution Strategy**: Plan parallel vs serial execution
- **Verification Plan**: Define testing and validation

### 3. Parallel Execution

```bash
# Execute multiple agents simultaneously
Task(subagent_type="general-purpose", description="Task A", prompt="...")
Task(subagent_type="general-purpose", description="Task B", prompt="...")
Task(subagent_type="general-purpose", description="Task C", prompt="...")
```

**Best Practices:**
- Limit to ONE task `in_progress` at a time in todo list
- Use parallel coordinator for complex dependency management
- Monitor context window usage with `/context`
- Create checkpoints after major milestones

## 🤖 Specialized Agents

### Core Research Agents (Enhanced from audio-enhancement-model)

#### Codebase Locator Agent
**Purpose**: Finds files, directories, and components (WHERE code lives)
**Best For**: Discovering project structure and locating relevant files
```bash
Task(subagent_type="codebase-locator",
     description="Find authentication components",
     prompt="Locate all files related to user authentication system")
```

#### Codebase Analyzer Agent
**Purpose**: Analyzes implementation details (HOW code works)
**Best For**: Understanding data flow, algorithms, and architectural patterns
```bash
Task(subagent_type="codebase-analyzer",
     description="Analyze JWT implementation",
     prompt="Analyze how JWT token validation works in the authentication system")
```

#### Research Synthesizer Agent
**Purpose**: Connects patterns and creates comprehensive insights
**Best For**: Combining findings from multiple agents into unified understanding
```bash
Task(subagent_type="research-synthesizer",
     description="Synthesize auth patterns",
     prompt="Create comprehensive understanding of authentication system from all research")
```

#### Web Research Specialist Agent
**Purpose**: External documentation and best practices research
**Best For**: Finding official docs, industry standards, troubleshooting guides
```bash
Task(subagent_type="web-research-specialist",
     description="Research JWT best practices",
     prompt="Find JWT security best practices and official documentation")
```

### Research Command (NEW)
**Purpose**: Comprehensive codebase investigation using multiple specialized agents
**Best For**: Complex research questions requiring systematic analysis
```bash
Task(subagent_type="research",
     description="Research authentication system",
     prompt="How does the authentication system work in this codebase?")
```

### Original Template Agents

#### Problem Solver Agent
**Purpose**: Systematic problem analysis and solution architecture
**Best For**: Complex requirement analysis, architectural decisions
```bash
Task(subagent_type="problem-solver",
     description="Analyze system requirements",
     prompt="Decompose this problem into independent tasks: [PROBLEM]")
```

#### Context Manager Agent
**Purpose**: Session continuity and thought process logging
**Best For**: Maintaining project state across sessions
```bash
Task(subagent_type="context-manager",
     description="Update project context",
     prompt="Document current progress and create session summary")
```

#### Parallel Coordinator Agent
**Purpose**: Multi-agent orchestration and dependency management
**Best For**: Complex workflows with multiple parallel streams
```bash
Task(subagent_type="parallel-coordinator",
     description="Orchestrate parallel development",
     prompt="Coordinate execution of [N] parallel tasks with dependencies")
```

## 🧠 Context Management

### Session Continuity Commands

```bash
# Check current context usage
/context

# Compress conversation history
/compact

# Hard reset (use when context drifts)
/clear

# Resume specific session
claude --resume [sessionId]

# Fork from existing session
claude --fork-session
```

### Automatic Context Preservation

The template automatically maintains:

- **Decision Log** (`session-data/decisions.jsonl`): All architectural decisions with rationale
- **Progress Checkpoints** (`session-data/checkpoints.jsonl`): Major milestones and state snapshots
- **Context State** (`session-data/context-state.json`): Current project understanding
- **Session Logs** (`logs/session-YYYYMMDD.md`): Daily activity logs

### Manual Context Updates

```python
# Log important decisions
from templates.context_preservation import ContextManager
cm = ContextManager()

cm.log_decision(
    decision="Use FastAPI over Flask",
    rationale="Better async support and auto documentation",
    alternatives=["Flask", "Django"],
    confidence=8,
    tags=["architecture", "web-framework"]
)

# Create progress checkpoint
cm.create_checkpoint(
    objective="Set up authentication system",
    achievements=["JWT implementation", "User model"],
    challenges=["OAuth integration complexity"],
    current_state="Basic auth working, OAuth pending",
    next_actions=["Implement OAuth flow", "Add tests"]
)
```

## 📋 Todo List Management

### Automated Task Decomposition

```python
from templates.todo_management import TodoManager

manager = TodoManager()
plan = manager.generate_execution_plan(
    problem="Build e-commerce platform with payment processing",
    context="Python/FastAPI backend, React frontend"
)

# Get Claude-compatible todo format
claude_todos = manager.get_claude_todo_format(plan["tasks"])
```

### Manual Todo Management

```python
# Update task status
manager.update_task_status(
    task_id="task-123",
    status="completed",
    log_entry="Implemented user authentication"
)

# Identify parallel opportunities
parallel_groups = manager.identify_parallel_opportunities(tasks)
print(parallel_groups)
# {'stage_0': ['task-1', 'task-2'], 'stage_1': ['task-3']}
```

## ⚡ Parallel Execution Patterns

### Pattern 1: Independent Research
```bash
# Launch parallel research agents
Task(subagent_type="general-purpose", description="Research auth options")
Task(subagent_type="general-purpose", description="Research payment APIs")
Task(subagent_type="general-purpose", description="Research deployment options")
```

### Pattern 2: Component-Based Development
```bash
# Parallel component implementation
Task(subagent_type="general-purpose", description="User management module")
Task(subagent_type="general-purpose", description="Product catalog module")
Task(subagent_type="general-purpose", description="Order processing module")
```

### Pattern 3: Layered Implementation
```bash
# Stage 1: Foundation (parallel)
Task(subagent_type="general-purpose", description="Database models")
Task(subagent_type="general-purpose", description="API endpoints")
Task(subagent_type="general-purpose", description="UI components")

# Stage 2: Integration (after stage 1)
Task(subagent_type="general-purpose", description="End-to-end testing")
```

## 🔧 Python Integration

### Common Frameworks Supported

- **Web**: FastAPI, Flask, Django
- **ML/AI**: PyTorch, TensorFlow, scikit-learn
- **Data**: Pandas, NumPy, Jupyter notebooks
- **Testing**: pytest, unittest, coverage
- **Code Quality**: ruff, mypy, black, pre-commit

### Example Integration

```python
# templates/project_setup.py
from todo_management import TodoManager
from context_preservation import ContextManager

def setup_fastapi_project(requirements: str):
    """Setup FastAPI project with proper decomposition"""

    manager = TodoManager()
    context_mgr = ContextManager()

    # Decompose requirements
    plan = manager.generate_execution_plan(requirements)

    # Log architectural decisions
    context_mgr.log_decision(
        decision="FastAPI for web framework",
        rationale="Async support and automatic OpenAPI docs",
        tags=["architecture", "web"]
    )

    return plan["claude_format"]
```

## 🧪 Testing and Quality

### Automated Quality Checks

```bash
# Add to CLAUDE.md for automatic execution
uv run python -m pytest tests/
uv run ruff check .
uv run mypy src/
```

### Integration with Template

```python
# Auto-execute after code changes
from templates.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Add quality gates to execution plan
quality_tasks = [
    "Run pytest test suite",
    "Execute ruff linting",
    "Perform mypy type checking",
    "Check test coverage"
]
```

## 📊 Monitoring and Analytics

### Execution Metrics

```python
from templates.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()
results = orchestrator.execute_plan(plan, executions)

print(f"Success rate: {results['completed_tasks']}/{results['total_tasks']}")
print(f"Execution time: {results['total_duration']} minutes")
```

### Context Window Optimization

```bash
# Monitor token usage
/context

# Optimize before hitting limits
/compact

# Use specialized agents to preserve main context
Task(subagent_type="general-purpose", description="Research task",
     prompt="Research and summarize findings for main context")
```

## 🚨 Common Pitfalls and Solutions

### Context Window Management
- **Problem**: Token limit reached mid-task
- **Solution**: Use `/compact` proactively, delegate to subagents

### Dependency Conflicts
- **Problem**: Parallel tasks creating file conflicts
- **Solution**: Use Git worktrees, clear interface definitions

### Session Continuity
- **Problem**: Lost context between sessions
- **Solution**: Regular checkpoints, structured logging

### Agent Coordination
- **Problem**: Duplicated work across agents
- **Solution**: Clear task boundaries, regular sync points

## 🔄 Advanced Workflows

### Multi-Session Projects

```bash
# Session 1: Architecture and planning
claude --continue
# Use problem-solver and context-manager agents

# Session 2: Parallel implementation
claude --fork-session
# Use parallel-coordinator for multi-agent execution

# Session 3: Integration and testing
claude --fork-session
# Focus on quality gates and deployment
```

### Cross-Agent Communication

```python
# Share context between agents via structured files
context_mgr = ContextManager()
context_mgr.create_checkpoint(
    objective="API implementation",
    achievements=["User endpoints complete"],
    next_actions=["Frontend integration needed"]
)

# Next agent can read checkpoint for context
```

## 🛠️ Utility Scripts (NEW)

The template includes utility scripts in the `hack/` directory for enhanced agent workflows:

### Project Structure Analysis
```bash
# Full project analysis for agents
bash hack/understand_project_structure.sh

# Analyze specific directories
bash hack/understand_project_structure.sh src tests templates
```

### Metadata Generation
```bash
# Generate research metadata
bash hack/project_metadata.sh

# Generate research filename
bash hack/project_metadata.sh -f "authentication system"
```

These scripts are used automatically by research agents to understand project structure and generate comprehensive documentation.

## 🎯 Enhanced Features

### Research Command System
- **Systematic Investigation**: Multi-agent coordination for complex questions
- **Evidence-Based**: All findings include specific file:line references
- **External Integration**: Combines codebase analysis with best practices
- **Pattern Recognition**: Identifies architectural decisions and design patterns

### Advanced Agent Architecture
- **Specialized Agents**: Purpose-built for specific research tasks
- **Tool Restrictions**: Read-only operations for safety
- **Context Optimization**: Strategic delegation to preserve main context
- **Structured Output**: Consistent formats for synthesis and documentation

## 📚 Examples and Templates

See `examples/` directory for:
- FastAPI REST API setup
- PyTorch ML pipeline
- Data analysis workflow
- Multi-microservice architecture
- Integrated research workflows (NEW)

## 🤝 Contributing

To extend this template:

1. Add new specialized agents in `.claude/agents/`
2. Create workflow commands in `.claude/commands/`
3. Add utility scripts in `hack/`
4. Update documentation with new patterns
5. Test with realistic scenarios

**Important**: This template does not include Claude as a co-author in commits to maintain clean git history.

## 📄 License

This template is designed for effective Claude Code usage. Adapt it to your specific needs and coding patterns.