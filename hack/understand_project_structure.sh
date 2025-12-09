#!/bin/bash
#
# understand_project_structure.sh - Analyze project structure for Claude Code agents
#
# This script provides a comprehensive overview of the project structure,
# optimized for Claude Code agents to understand codebase organization.
#
# Usage:
#   bash hack/understand_project_structure.sh              # Full analysis
#   bash hack/understand_project_structure.sh src tests   # Targeted analysis

set -euo pipefail

# Color definitions for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
MAX_FILES_PER_DIR=20
MAX_DEPTH=4
IGNORE_DIRS=(".git" "__pycache__" "node_modules" ".pytest_cache" ".mypy_cache" "*.egg-info" ".venv" "venv" "env")
IGNORE_FILES=("*.pyc" "*.pyo" "*.log" "*.tmp" "*.swp" ".DS_Store")

# Helper functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_subheader() {
    echo -e "${CYAN}--- $1 ---${NC}"
}

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Build ignore patterns for find command
build_ignore_patterns() {
    local ignore_pattern=""
    for dir in "${IGNORE_DIRS[@]}"; do
        if [[ -z "$ignore_pattern" ]]; then
            ignore_pattern="( -name '$dir' -prune )"
        else
            ignore_pattern="$ignore_pattern -o ( -name '$dir' -prune )"
        fi
    done
    echo "$ignore_pattern -o"
}

# Analyze project overview
analyze_project_overview() {
    print_header "PROJECT OVERVIEW"

    echo "Repository: $(basename "$(pwd)")"
    echo "Path: $(pwd)"
    echo "Analysis Date: $(date '+%Y-%m-%d %H:%M:%S')"

    if [[ -d .git ]]; then
        echo "Git Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')"
        echo "Git Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
    else
        echo "Git Status: Not a git repository"
    fi

    echo ""
}

# Analyze directory structure
analyze_directory_structure() {
    print_header "DIRECTORY STRUCTURE"

    local target_dirs=("$@")
    local ignore_patterns
    ignore_patterns=$(build_ignore_patterns)

    if [[ ${#target_dirs[@]} -eq 0 ]]; then
        print_info "Analyzing complete project structure (depth: $MAX_DEPTH)"
        eval "find . -maxdepth $MAX_DEPTH -type d $ignore_patterns -print" | \
            grep -v '^.$' | sort | head -50
    else
        for dir in "${target_dirs[@]}"; do
            if [[ -d "$dir" ]]; then
                print_info "Analyzing directory: $dir"
                eval "find \"$dir\" -maxdepth $MAX_DEPTH -type d $ignore_patterns -print" | \
                    sort | head -30
            else
                print_warning "Directory not found: $dir"
            fi
        done
    fi

    echo ""
}

# Analyze file types and distributions
analyze_file_distribution() {
    print_header "FILE TYPE DISTRIBUTION"

    local target_dirs=("$@")
    local search_path="."

    if [[ ${#target_dirs[@]} -gt 0 ]]; then
        search_path="${target_dirs[*]}"
    fi

    print_subheader "File Extensions"
    find $search_path -type f \( ! -path "*/.git/*" ! -path "*/__pycache__/*" ! -path "*/node_modules/*" \) -name "*.*" | \
        grep -o '\.[^./]*$' | sort | uniq -c | sort -rn | head -20

    echo ""

    print_subheader "Files by Category"

    # Python files
    local py_count
    py_count=$(find $search_path -name "*.py" -type f 2>/dev/null | wc -l)
    if [[ $py_count -gt 0 ]]; then
        echo "Python files: $py_count"
    fi

    # JavaScript/TypeScript files
    local js_count
    js_count=$(find $search_path \( -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" \) -type f 2>/dev/null | wc -l)
    if [[ $js_count -gt 0 ]]; then
        echo "JavaScript/TypeScript files: $js_count"
    fi

    # Configuration files
    local config_count
    config_count=$(find $search_path \( -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" -o -name "*.ini" \) -type f 2>/dev/null | wc -l)
    if [[ $config_count -gt 0 ]]; then
        echo "Configuration files: $config_count"
    fi

    # Documentation files
    local doc_count
    doc_count=$(find $search_path \( -name "*.md" -o -name "*.rst" -o -name "*.txt" \) -type f 2>/dev/null | wc -l)
    if [[ $doc_count -gt 0 ]]; then
        echo "Documentation files: $doc_count"
    fi

    # Test files
    local test_count
    test_count=$(find $search_path \( -name "*test*" -o -name "*spec*" \) -type f 2>/dev/null | wc -l)
    if [[ $test_count -gt 0 ]]; then
        echo "Test files: $test_count"
    fi

    echo ""
}

# Generate analysis summary
generate_summary() {
    print_header "ANALYSIS SUMMARY FOR CLAUDE AGENTS"

    print_subheader "Quick Navigation Guide"
    echo "Primary source code:"
    for dir in "src" "lib" "app"; do
        if [[ -d "$dir" ]]; then
            echo "  • $dir/ - Contains main implementation files"
        fi
    done

    echo ""
    echo "Configuration and setup:"
    for file in "CLAUDE.md" "pyproject.toml" "package.json" "requirements.txt"; do
        if [[ -f "$file" ]]; then
            echo "  • $file - Project configuration"
        fi
    done

    echo ""
    print_subheader "Agent Usage Recommendations"
    echo "• Use 'codebase-locator' agent to find specific components in the directories above"
    echo "• Use 'codebase-analyzer' agent to understand implementation details"
    echo "• Check CLAUDE.md for project-specific commands and conventions"

    echo ""
}

# Main execution
main() {
    local target_dirs=("$@")

    analyze_project_overview
    analyze_directory_structure "${target_dirs[@]}"
    analyze_file_distribution "${target_dirs[@]}"

    # Only analyze all sections if no specific directories were requested
    if [[ ${#target_dirs[@]} -eq 0 ]]; then
        generate_summary
    else
        print_info "Targeted analysis complete for: ${target_dirs[*]}"
    fi
}

# Check if script is being sourced or executed
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi