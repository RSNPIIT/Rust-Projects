#!/usr/bin/env bash
# commit_each_file.sh
# Commits every single file / rename individually, generating 300+ separate commits.

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
    echo "Usage: ./commit_each_file.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dry-run       Show all file commits without executing"
    echo "  --commit-only   Commit every file individually locally (300+ commits, no push)"
    echo "  --push          Commit and push after EVERY single file (creates continuous push events)"
    echo "  --from <NUM>    Resume starting from file index NUM (e.g. --from 50)"
    echo "  --delay <SEC>   Delay in seconds between pushes (default: 1)"
    echo "  --remote <NAME> Git remote name (default: origin)"
    echo "  --branch <NAME> Git branch name (default: current branch or main)"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./commit_each_file.sh --dry-run"
    echo "  ./commit_each_file.sh --commit-only"
    echo "  ./commit_each_file.sh --push --delay 1"
    echo "  ./commit_each_file.sh --from 120 --push"
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

# If no mode given, prompt if interactive or default to commit-only
if [ "$DO_PUSH" = false ] && [ "$COMMIT_ONLY" = false ] && [ "$DRY_RUN" = false ]; then
    if [ -t 0 ]; then
        echo "========================================================="
        echo "🔥 300+ Single-File Commits Automation"
        echo "========================================================="
        echo "Please select an execution mode:"
        echo "  1) Commit and Push EACH file individually to GitHub (~300 commits & pushes) [Recommended]"
        echo "  2) Commit locally each file one-by-one (~300 local commits instantly, push all later)"
        echo "  3) Dry run preview (Inspect all ~300 planned commits)"
        echo ""
        read -r -p "Enter choice [1/2/3] (default 1): " choice
        case "$choice" in
            2) COMMIT_ONLY=true ;;
            3) DRY_RUN=true ;;
            *) DO_PUSH=true ;;
        esac
    else
        echo "ℹ️ Non-interactive session: defaulting to --commit-only."
        COMMIT_ONLY=true
    fi
fi

echo "========================================================="
echo "🦀 Single-File Commit & Push Automation"
echo "========================================================="
echo "Repository : $REPO_ROOT"
echo "Branch     : $BRANCH"
echo "Remote     : $REMOTE"
echo "Mode       : $([ "$DRY_RUN" = true ] && echo "DRY RUN" || ([ "$DO_PUSH" = true ] && echo "COMMIT AND PUSH PER FILE" || echo "COMMIT ONLY"))"
echo "Start From : Item #$FROM_NUM"
echo "Push Delay : ${DELAY_SECONDS}s"
echo "========================================================="
echo ""

# Extract all staged renames
RENAMES=()
while IFS= read -r line; do
    if [[ "$line" =~ ^R[[:space:]]+(.*)[[:space:]]-\>[[:space:]]+(.*)$ ]]; then
        old_file="${BASH_REMATCH[1]}"
        new_file="${BASH_REMATCH[2]}"
        RENAMES+=("$old_file::$new_file")
    fi
done < <(git status --porcelain | grep '^R' | sort)

TOTAL_FILES=${#RENAMES[@]}

if [ "$TOTAL_FILES" -eq 0 ]; then
    echo "⚠️ No staged renames detected in git status."
    echo "   If you have unstaged changes, stage them first or check 'git status'."
    exit 0
fi

echo "📋 Found $TOTAL_FILES staged files ready for individual commits."
echo ""

INDEX=0
COMMITTED_COUNT=0

for item in "${RENAMES[@]}"; do
    INDEX=$((INDEX + 1))

    if [ "$INDEX" -lt "$FROM_NUM" ]; then
        continue
    fi

    old_f="${item%::*}"
    new_f="${item#*::}"

    # Extract target project name and file basename
    proj_dir="$(dirname "$new_f")"
    base_file="$(basename "$new_f")"
    clean_proj="${proj_dir//_/ }"

    commit_msg="refactor($proj_dir): rename $old_f -> $new_f"

    echo "[$INDEX/$TOTAL_FILES] Committing: $new_f"
    echo "       Message: \"$commit_msg\""

    if [ "$DRY_RUN" = true ]; then
        echo "       [Dry Run] git commit '$old_f' '$new_f' -m '$commit_msg'"
        if [ "$DO_PUSH" = true ]; then
            echo "       [Dry Run] git push $REMOTE $BRANCH (delay ${DELAY_SECONDS}s)"
        fi
    else
        git commit "$old_f" "$new_f" -m "$commit_msg"
        COMMITTED_COUNT=$((COMMITTED_COUNT + 1))

        if [ "$DO_PUSH" = true ]; then
            echo "       🚀 Pushing commit to $REMOTE/$BRANCH..."
            git push "$REMOTE" "$BRANCH" || {
                echo "❌ Push failed at item $INDEX ($new_f)."
                echo "   Resume anytime using: ./commit_each_file.sh --from $INDEX --push"
                exit 1
            }
            sleep "$DELAY_SECONDS"
        fi
    fi
done

# If file_changer.sh is untracked, commit it at the end
if [ -f "file_changer.sh" ] && git status --porcelain file_changer.sh | grep -q .; then
    echo ""
    echo "📦 Staging utility script: file_changer.sh"
    if [ "$DRY_RUN" = true ]; then
        echo "   [Dry Run] git add file_changer.sh"
        echo "   [Dry Run] git commit -m 'chore: add directory renaming script'"
    else
        git add file_changer.sh
        git commit -m "chore: add directory renaming script"
        if [ "$DO_PUSH" = true ]; then
            git push "$REMOTE" "$BRANCH" || true
        fi
    fi
fi

echo ""
echo "========================================================="
echo "🎉 Complete! Successfully processed $COMMITTED_COUNT / $TOTAL_FILES files."
if [ "$COMMIT_ONLY" = true ] && [ "$COMMITTED_COUNT" -gt 0 ]; then
    echo "💡 All $COMMITTED_COUNT individual commits created locally!"
    echo "   To push all commits to GitHub in one command, run:"
    echo "   git push $REMOTE $BRANCH"
fi
echo "========================================================="
