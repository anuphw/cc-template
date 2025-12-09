# Utility Scripts

This directory contains utility scripts that enhance Claude Code workflows with automated project analysis and metadata generation.

## Scripts

### `understand_project_structure.sh`
**Purpose**: Comprehensive project analysis for research agents

**Usage**:
```bash
# Analyze entire project
bash hack/understand_project_structure.sh

# Analyze specific directories
bash hack/understand_project_structure.sh src tests templates
```

**Features**:
- File type analysis and categorization
- Dependency detection and mapping
- Configuration file identification
- Test file discovery
- Documentation file cataloging
- Project structure visualization

**Output**: Structured analysis used by research agents to understand codebase organization

### `project_metadata.sh`
**Purpose**: Generate metadata for research and documentation

**Usage**:
```bash
# Generate all metadata
bash hack/project_metadata.sh --all

# Generate research filename for specific topic
bash hack/project_metadata.sh --filename "authentication system"

# Generate technology stack summary
bash hack/project_metadata.sh --tech-stack

# Generate project structure summary
bash hack/project_metadata.sh --structure
```

**Features**:
- Technology stack detection
- Project structure analysis
- Research filename generation
- Metadata export in JSON format

**Output**: JSON metadata files in `session-data/` directory

## Integration with Agents

These scripts are automatically used by research agents to:

1. **Understand Project Context**: Before analyzing code, agents run structure analysis
2. **Generate Documentation**: Metadata scripts help create comprehensive research reports
3. **Maintain Consistency**: Standardized analysis ensures consistent research quality
4. **Optimize Search**: Structure analysis helps agents focus on relevant files

## Customization

To extend these scripts for your project:

1. **Add File Type Detection**: Modify patterns in `understand_project_structure.sh`
2. **Include Custom Metadata**: Extend JSON structure in `project_metadata.sh`
3. **Add Project-Specific Analysis**: Create additional scripts following the same patterns
4. **Update Agent Configurations**: Reference new scripts in agent prompts

## Requirements

- **Bash 4.0+**: For associative arrays and modern features
- **jq**: For JSON processing (optional but recommended)
- **tree**: For directory visualization (optional)
- **find, grep, wc**: Standard Unix utilities

Most systems will have these tools installed by default.