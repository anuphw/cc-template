#!/bin/bash

# Project metadata generation script for research agents
# Used by research agents to understand project context and generate documentation

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# Default output directory
OUTPUT_DIR="${PROJECT_ROOT}/session-data"
mkdir -p "$OUTPUT_DIR"

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Generate project metadata for research agents.

OPTIONS:
    -h, --help              Show this help message
    -o, --output DIR        Output directory (default: session-data)
    -f, --filename TOPIC    Generate research filename for topic
    -t, --tech-stack        Generate technology stack summary
    -s, --structure         Generate project structure summary
    -a, --all              Generate all metadata

EXAMPLES:
    $0 --all                                    # Generate all metadata
    $0 --filename "authentication system"      # Generate research filename
    $0 --tech-stack                            # Generate tech stack summary
    $0 --structure                             # Generate structure summary

EOF
}

generate_research_filename() {
    local topic="$1"
    local safe_topic
    safe_topic=$(echo "$topic" | tr '[:upper:]' '[:lower:]' | tr -c '[:alnum:]' '-' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
    echo "research_${safe_topic}_${TIMESTAMP}.md"
}

generate_tech_stack() {
    local output_file="$OUTPUT_DIR/tech_stack_${TIMESTAMP}.json"

    cat > "$output_file" << 'EOF'
{
  "detected_technologies": [],
  "package_managers": [],
  "frameworks": [],
  "languages": [],
  "databases": [],
  "testing_frameworks": [],
  "build_tools": [],
  "deployment": [],
  "ci_cd": [],
  "documentation": [],
  "last_updated": ""
}
EOF

    # Detect technologies based on files present
    local tech_stack=""

    if [[ -f "$PROJECT_ROOT/package.json" ]]; then
        tech_stack=$(jq '.detected_technologies += ["Node.js", "JavaScript"] | .package_managers += ["npm"]' "$output_file")
        echo "$tech_stack" > "$output_file"
    fi

    if [[ -f "$PROJECT_ROOT/requirements.txt" ]] || [[ -f "$PROJECT_ROOT/pyproject.toml" ]]; then
        tech_stack=$(jq '.detected_technologies += ["Python"] | .package_managers += ["pip"]' "$output_file")
        echo "$tech_stack" > "$output_file"
    fi

    if [[ -f "$PROJECT_ROOT/Cargo.toml" ]]; then
        tech_stack=$(jq '.detected_technologies += ["Rust"] | .package_managers += ["cargo"]' "$output_file")
        echo "$tech_stack" > "$output_file"
    fi

    if [[ -f "$PROJECT_ROOT/go.mod" ]]; then
        tech_stack=$(jq '.detected_technologies += ["Go"] | .package_managers += ["go mod"]' "$output_file")
        echo "$tech_stack" > "$output_file"
    fi

    # Update timestamp
    tech_stack=$(jq --arg timestamp "$(date -Iseconds)" '.last_updated = $timestamp' "$output_file")
    echo "$tech_stack" > "$output_file"

    echo "Tech stack metadata generated: $output_file"
}

generate_project_structure() {
    local output_file="$OUTPUT_DIR/project_structure_${TIMESTAMP}.json"

    # Generate project structure
    cat > "$output_file" << EOF
{
  "project_root": "$PROJECT_ROOT",
  "generated_at": "$(date -Iseconds)",
  "directory_structure": {},
  "important_files": [],
  "config_files": [],
  "source_directories": [],
  "test_directories": [],
  "documentation_files": []
}
EOF

    # Add directory structure
    if command -v tree >/dev/null 2>&1; then
        tree -J "$PROJECT_ROOT" > /tmp/tree_output.json 2>/dev/null || true
        if [[ -s /tmp/tree_output.json ]]; then
            jq --slurpfile tree /tmp/tree_output.json '.directory_structure = $tree[0]' "$output_file" > /tmp/updated.json
            mv /tmp/updated.json "$output_file"
            rm -f /tmp/tree_output.json
        fi
    fi

    # Find important files
    local important_files=()
    while IFS= read -r -d '' file; do
        important_files+=("$(realpath --relative-to="$PROJECT_ROOT" "$file")")
    done < <(find "$PROJECT_ROOT" -maxdepth 2 \( -name "README*" -o -name "CHANGELOG*" -o -name "LICENSE*" -o -name "CONTRIBUTING*" -o -name "CLAUDE.md" \) -type f -print0 2>/dev/null || true)

    if [[ ${#important_files[@]} -gt 0 ]]; then
        printf -v important_files_json '%s\n' "${important_files[@]}" | jq -R . | jq -s .
        jq --argjson files "$important_files_json" '.important_files = $files' "$output_file" > /tmp/updated.json
        mv /tmp/updated.json "$output_file"
    fi

    echo "Project structure metadata generated: $output_file"
}

generate_all_metadata() {
    echo "Generating all project metadata..."
    generate_tech_stack
    generate_project_structure
    echo "All metadata generation complete."
}

main() {
    case "${1:-}" in
        -h|--help)
            usage
            exit 0
            ;;
        -f|--filename)
            if [[ -z "${2:-}" ]]; then
                echo "Error: Topic required for filename generation" >&2
                exit 1
            fi
            generate_research_filename "$2"
            exit 0
            ;;
        -t|--tech-stack)
            generate_tech_stack
            exit 0
            ;;
        -s|--structure)
            generate_project_structure
            exit 0
            ;;
        -a|--all)
            generate_all_metadata
            exit 0
            ;;
        "")
            # Default behavior - show usage
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'" >&2
            usage
            exit 1
            ;;
    esac
}

main "$@"