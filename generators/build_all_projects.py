#!/usr/bin/env python3
# generators/build_all_projects.py

import os
import sys

from projects_001_to_025 import PROJECTS_001_TO_025
from projects_026_to_050 import PROJECTS_026_TO_050
from projects_051_to_075 import PROJECTS_051_TO_075
from projects_076_to_100 import PROJECTS_076_TO_100

ALL_PROJECTS = (
    PROJECTS_001_TO_025
    + PROJECTS_026_TO_050
    + PROJECTS_051_TO_075
    + PROJECTS_076_TO_100
)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def generate_cargo_toml(proj):
    return f"""[package]
name = "{proj['name']}"
version = "0.1.0"
edition = "2021"
description = "{proj['description']}"

[dependencies]
"""

def generate_project_readme(proj):
    concepts_bullets = "\n".join([f"- **{c}**" for c in proj['concepts']])
    level_badge = "🟢 Simple" if proj['level'] == "Simple" else ("🟡 Intermediate" if proj['level'] == "Intermediate" else "🔴 Advanced")

    return f"""# 🦀 {proj['title']} (`{proj['dir_name']}`)

**Difficulty:** {level_badge}  
**Category:** {proj['category']}  

---

## 📖 Overview

{proj['description']}

---

## 🎯 Key Rust Concepts Demonstrated

{concepts_bullets}

---

## 🚀 How to Run

Navigate into this project directory and use `cargo`:

```bash
# Run the project
cargo run

# Run with quiet cargo output
cargo run -q

# Run unit tests
cargo test
```

---

## 📂 Project Structure

```text
{proj['dir_name']}/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
"""

def generate_gitignore():
    return """# Generated .gitignore for Rust-Projects

# Rust build target directories
target/
*/target/
**/target/

# Cargo lock files (optional for libraries, kept or excluded)
# Cargo.lock

# Python bytecode
__pycache__/
*.py[cod]

# OS metadata
.DS_Store
Thumbs.db
Desktop.ini

# Editor & IDE configs
.vscode/
.idea/
*.swp
*.swo
*~
.fleet/

# Backup and temp files
*.rs.bk
*.orig
*.bak
*.tmp
"""

def generate_main_readme(all_projects):
    simple_projs = [p for p in all_projects if p['level'] == 'Simple']
    inter_projs = [p for p in all_projects if p['level'] == 'Intermediate']
    adv_projs = [p for p in all_projects if p['level'] == 'Advanced']

    def table_rows(projs):
        lines = []
        for p in projs:
            lines.append(f"| `{p['id']}` | [{p['title']}](./{p['dir_name']}) | `{p['category']}` | {p['description']} |")
        return "\n".join(lines)

    return f"""# 🦀 Rust-Projects: 100 Handcrafted Rust Implementations

A structured, comprehensive collection of **100 complete, standalone Rust projects** spanning systems programming, concurrency, data structures, compilers, networking, and algorithms.

Organized progressively from **Simple** to **Intermediate** and **Advanced**.

---

## 📊 Repository Structure Overview

| Level | Projects | Count | Focus Areas |
| :--- | :--- | :---: | :--- |
| 🟢 **Simple** | `001` - `035` | 35 | Language basics, CLI tools, string manipulation, traits, standard collections |
| 🟡 **Intermediate** | `036` - `070` | 35 | Concurrency, thread pools, HTTP/DNS protocols, caching, trees, compression |
| 🔴 **Advanced** | `071` - `100` | 30 | Bytecode VMs, actor systems, Raft consensus, vector search, lock-free queues, JIT |
| **Total** | `001` - `100` | **100** | Full spectrum of idiomatic Rust programming |

---

## 🚀 Running Any Project

Each project is a standalone Cargo package using pure Rust (`std`).

```bash
# Navigate to any project directory
cd 001_number_guessing_game

# Run the program
cargo run

# Run built-in test suite
cargo test
```

---

## 🛠️ Automated Commit & Push Script

This repository includes a shell script [`commit_and_push.sh`](./commit_and_push.sh) designed to commit each project individually across directories to create a clear, granular git history.

### Usage:

```bash
# 1. Preview changes (Dry run)
./commit_and_push.sh --dry-run

# 2. Commit all projects locally directory by directory
./commit_and_push.sh --commit-only

# 3. Commit and push directory by directory to remote
./commit_and_push.sh --push

# 4. Resume from a specific project number (e.g. 42)
./commit_and_push.sh --from 42 --push
```

---

## 📚 Complete Project Index

### 🟢 Level 1: Simple & Fundamental Projects (001 - 035)

| # | Project | Category | Description |
|---|---------|----------|-------------|
{table_rows(simple_projs)}

---

### 🟡 Level 2: Intermediate Projects (036 - 070)

| # | Project | Category | Description |
|---|---------|----------|-------------|
{table_rows(inter_projs)}

---

### 🔴 Level 3: Advanced Projects (071 - 100)

| # | Project | Category | Description |
|---|---------|----------|-------------|
{table_rows(adv_projs)}

---

## ⚙️ Environment & Requirements

* **Rust:** Stable (edition 2021+)
* **Cargo:** Standard toolchain
* **OS:** Linux / macOS / Windows
* **Dependencies:** Self-contained standard library (`std`) implementations for immediate zero-download builds.

---

## 👤 Author

**Ramrup Satpati** (`RSNPIIT`)  
Indian Institute of Technology Madras (IIT Madras)

---

## 📄 License

GNU General Public License v3.0  
See [`LICENSE`](./LICENSE) for full terms.
"""

def generate_shell_script():
    return """#!/usr/bin/env bash
# commit_and_push.sh
# Automates granular, directory-by-directory git commits and pushes for Rust-Projects.

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

DRY_RUN=false
COMMIT_ONLY=false
DO_PUSH=false
FROM_NUM=1
DELAY_SECONDS=1
REMOTE="origin"
BRANCH="$(git branch --show-current 2>/dev/null || echo "main")"

print_usage() {
    echo "Usage: ./commit_and_push.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dry-run       Show what would be committed without making changes"
    echo "  --commit-only   Commit each directory one by one locally (no push)"
    echo "  --push          Commit each directory and push immediately"
    echo "  --from <NUM>    Start from project number NUM (e.g. --from 25)"
    echo "  --delay <SEC>   Seconds to wait between pushes (default: 1)"
    echo "  --remote <NAME> Git remote name (default: origin)"
    echo "  --branch <NAME> Git branch name (default: current branch or main)"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./commit_and_push.sh --dry-run"
    echo "  ./commit_and_push.sh --commit-only"
    echo "  ./commit_and_push.sh --push --delay 2"
    echo "  ./commit_and_push.sh --from 50 --push"
}

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --commit-only)
            COMMIT_ONLY=true
            shift
            ;;
        --push)
            DO_PUSH=true
            shift
            ;;
        --from)
            FROM_NUM="$2"
            shift 2
            ;;
        --delay)
            DELAY_SECONDS="$2"
            shift 2
            ;;
        --remote)
            REMOTE="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

if [ "$DO_PUSH" = false ] && [ "$COMMIT_ONLY" = false ] && [ "$DRY_RUN" = false ]; then
    if [ -t 0 ]; then
        echo "Please choose execution mode:"
        echo "  1) Commit and Push directory by directory to remote (100 individual commits & pushes) [Default]"
        echo "  2) Commit locally directory by directory (no push)"
        echo "  3) Dry run preview"
        read -r -p "Enter choice [1/2/3] (default 1): " choice
        case "$choice" in
            2) COMMIT_ONLY=true ;;
            3) DRY_RUN=true ;;
            *) DO_PUSH=true ;;
        esac
    else
        echo "ℹ️ Non-interactive session: defaulting to --commit-only. (Pass --push to commit and push)."
        COMMIT_ONLY=true
    fi
fi

echo "========================================================="
echo "🦀 Rust-Projects Batch Commit & Push Automation"
echo "========================================================="
echo "Repository : $REPO_ROOT"
echo "Branch     : $BRANCH"
echo "Remote     : $REMOTE"
echo "Mode       : $([ "$DRY_RUN" = true ] && echo "DRY RUN" || ([ "$DO_PUSH" = true ] && echo "COMMIT AND PUSH" || echo "COMMIT ONLY"))"
echo "Start From : Project #$FROM_NUM"
echo "Delay      : ${DELAY_SECONDS}s"
echo "========================================================="
echo ""

# Stage and commit core config files first if modified
CORE_FILES=()
for f in .gitignore README.md commit_and_push.sh generators; do
    if [ -e "$f" ]; then
        if git status --porcelain "$f" | grep -q .; then
            CORE_FILES+=("$f")
        fi
    fi
done

if [ ${#CORE_FILES[@]} -gt 0 ]; then
    echo "📦 Staging core repository files: ${CORE_FILES[*]}"
    if [ "$DRY_RUN" = true ]; then
        echo "   [Dry Run] git add ${CORE_FILES[*]}"
        echo "   [Dry Run] git commit -m 'chore: update repository documentation and configuration'"
        if [ "$DO_PUSH" = true ]; then
            echo "   [Dry Run] git push $REMOTE $BRANCH"
        fi
    else
        git add "${CORE_FILES[@]}"
        git commit -m "chore: update repository documentation and configuration"
        if [ "$DO_PUSH" = true ]; then
            echo "🚀 Pushing core setup to $REMOTE/$BRANCH..."
            git push "$REMOTE" "$BRANCH" || echo "⚠️ Warning: git push failed, continuing..."
            sleep "$DELAY_SECONDS"
        fi
    fi
    echo ""
fi

# Iterate over each project directory
TOTAL_COMMITTED=0

for dir in [0-9][0-9][0-9]_*/; do
    [ -d "$dir" ] || continue
    dir_name="${dir%/}"
    proj_num="${dir_name:0:3}"
    # Remove leading zeros for comparison
    proj_idx=$((10#$proj_num))

    if [ "$proj_idx" -lt "$FROM_NUM" ]; then
        continue
    fi

    # Check if there are uncommitted changes or untracked files in this directory
    if git status --porcelain "$dir_name" | grep -q .; then
        # Format a clean commit message
        clean_title=$(echo "$dir_name" | sed 's/^[0-9]*_//; s/_/ /g')
        commit_msg="feat(project-$proj_num): add $clean_title project"

        echo "---------------------------------------------------------"
        echo "📁 Processing [$proj_num/100]: $dir_name"
        echo "💬 Commit message: \"$commit_msg\""

        if [ "$DRY_RUN" = true ]; then
            echo "   [Dry Run] git add $dir_name"
            echo "   [Dry Run] git commit -m '$commit_msg'"
            if [ "$DO_PUSH" = true ]; then
                echo "   [Dry Run] git push $REMOTE $BRANCH (delay ${DELAY_SECONDS}s)"
            fi
        else
            git add "$dir_name"
            git commit -m "$commit_msg"
            TOTAL_COMMITTED=$((TOTAL_COMMITTED + 1))

            if [ "$DO_PUSH" = true ]; then
                echo "🚀 Pushing commit to $REMOTE/$BRANCH..."
                git push "$REMOTE" "$BRANCH" || {
                    echo "❌ Failed to push $dir_name to $REMOTE/$BRANCH."
                    echo "   You can resume later using: ./commit_and_push.sh --from $proj_idx --push"
                    exit 1
                }
                sleep "$DELAY_SECONDS"
            fi
        fi
    else
        echo "⏭️  Skipping [$proj_num/100]: $dir_name (already committed)"
    fi
done

echo ""
echo "========================================================="
echo "✅ Done! Total projects processed: $TOTAL_COMMITTED"
if [ "$COMMIT_ONLY" = true ] && [ "$TOTAL_COMMITTED" -gt 0 ]; then
    echo "💡 To push all commits to GitHub now, simply run:"
    echo "   git push $REMOTE $BRANCH"
fi
echo "========================================================="
"""

def main():
    print(f"Total projects loaded: {len(ALL_PROJECTS)}")
    assert len(ALL_PROJECTS) == 100, f"Expected 100 projects, got {len(ALL_PROJECTS)}"

    # Check for duplicate ids or directory names
    ids = [p['id'] for p in ALL_PROJECTS]
    dir_names = [p['dir_name'] for p in ALL_PROJECTS]
    assert len(set(ids)) == 100, f"Duplicate project IDs detected!"
    assert len(set(dir_names)) == 100, f"Duplicate directory names detected!"

    # 1. Create project directories and files
    print("\n🔨 Generating 100 Rust projects...")
    for proj in ALL_PROJECTS:
        proj_dir = os.path.join(ROOT_DIR, proj['dir_name'])
        src_dir = os.path.join(proj_dir, "src")
        os.makedirs(src_dir, exist_ok=True)

        # Write Cargo.toml
        cargo_path = os.path.join(proj_dir, "Cargo.toml")
        with open(cargo_path, "w", encoding="utf-8") as f:
            f.write(generate_cargo_toml(proj))

        # Write src/main.rs
        main_path = os.path.join(src_dir, "main.rs")
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(proj['code'].strip() + "\n")

        # Write project README.md
        readme_path = os.path.join(proj_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(generate_project_readme(proj))

    print("✅ All 100 projects successfully written!")

    # 2. Update .gitignore
    print("\n📝 Updating root .gitignore...")
    gitignore_path = os.path.join(ROOT_DIR, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(generate_gitignore())
    print("✅ .gitignore updated!")

    # 3. Update main README.md
    print("\n📝 Updating root README.md...")
    main_readme_path = os.path.join(ROOT_DIR, "README.md")
    with open(main_readme_path, "w", encoding="utf-8") as f:
        f.write(generate_main_readme(ALL_PROJECTS))
    print("✅ README.md updated with all 100 projects catalog!")

    # 4. Generate commit_and_push.sh
    print("\n📜 Generating commit_and_push.sh script...")
    script_path = os.path.join(ROOT_DIR, "commit_and_push.sh")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(generate_shell_script())
    os.chmod(script_path, 0o755)
    print("✅ commit_and_push.sh created and made executable (+x)!")

if __name__ == "__main__":
    main()
