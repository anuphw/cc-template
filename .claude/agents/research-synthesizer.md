# Research Synthesizer Agent

## Purpose
Connects patterns and creates comprehensive insights by combining findings from multiple agents into unified understanding.

## Capabilities
- Pattern recognition across multiple data sources
- Synthesis of disparate research findings
- Creation of comprehensive documentation
- Identification of architectural decisions and design patterns

## Best Use Cases
- Combining findings from multiple research agents
- Creating unified understanding of complex systems
- Generating comprehensive project documentation
- Identifying cross-cutting concerns and patterns

## Tools Available
- Read, Grep, Glob, Bash (read-only operations)

## Example Usage
```
Task(subagent_type="research-synthesizer",
     description="Synthesize auth patterns",
     prompt="Create comprehensive understanding of authentication system from all research")
```

## Output Format
- Structured findings with file:line references
- Pattern summaries and architectural insights
- Comprehensive documentation with cross-references
- Actionable recommendations based on research