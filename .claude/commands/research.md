# Research Command

## Purpose
Comprehensive codebase investigation using multiple specialized agents for systematic analysis of complex questions.

## Capabilities
- Multi-agent coordination for research tasks
- Systematic investigation of codebase components
- Evidence-based findings with file:line references
- Integration of internal and external research

## Best Use Cases
- Complex research questions requiring systematic analysis
- Understanding large or unfamiliar codebases
- Architectural analysis and documentation
- Feature implementation research

## Usage
```bash
Task(subagent_type="research",
     description="Research authentication system",
     prompt="How does the authentication system work in this codebase?")
```

## Research Process
1. **Codebase Location**: Find relevant files and components
2. **Implementation Analysis**: Understand how code works
3. **Pattern Recognition**: Identify design patterns and decisions
4. **External Research**: Find best practices and documentation
5. **Synthesis**: Combine findings into comprehensive understanding

## Output Format
- Structured research report
- File:line references for all findings
- Architectural insights and patterns
- External documentation links
- Actionable recommendations