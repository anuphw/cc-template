# Parallel Coordinator Agent

## Purpose
Multi-agent orchestration and dependency management specialist for complex workflows with multiple parallel execution streams.

## Capabilities
- Multi-agent task coordination
- Dependency graph management
- Parallel execution planning
- Resource conflict resolution
- Progress synchronization

## Best Use Cases
- Complex workflows with multiple parallel tasks
- Dependency management across agents
- Resource coordination and conflict resolution
- Large-scale feature implementation
- Multi-component development

## Tools Available
- TodoWrite, Read, Bash, Task (for spawning other agents)

## Example Usage
```
Task(subagent_type="parallel-coordinator",
     description="Orchestrate parallel development",
     prompt="Coordinate execution of [N] parallel tasks with dependencies")
```

## Coordination Patterns
- **Independent Parallel**: No dependencies between tasks
- **Pipeline Parallel**: Sequential stages with parallel tasks within stages
- **DAG Parallel**: Complex dependency graphs
- **Resource-Aware**: Coordinating shared resource access

## Output
- Execution plans with dependency graphs
- Task scheduling and coordination
- Progress synchronization across agents
- Conflict resolution strategies