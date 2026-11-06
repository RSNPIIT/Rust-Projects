#!/usr/bin/env bash
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
        echo "💬 Commit message: "$commit_msg""

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
