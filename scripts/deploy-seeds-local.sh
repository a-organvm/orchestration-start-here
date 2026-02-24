#!/usr/bin/env bash
set -euo pipefail

# Deploy seed.yaml updates: commit + push any uncommitted/unpushed changes.
# Processes one organ at a time to respect 16GB RAM constraint.
#
# Usage:
#   ./scripts/deploy-seeds-local.sh              # Dry-run (default)
#   ./scripts/deploy-seeds-local.sh --commit     # Commit changes
#   ./scripts/deploy-seeds-local.sh --push       # Commit + push
#
# Order: ORGAN-IV → META → ORGAN-I → ORGAN-II → ORGAN-III → ORGAN-V → ORGAN-VI → ORGAN-VII

WORKSPACE="${HOME}/Workspace"
DRY_RUN=true
DO_PUSH=false
LOG_FILE="${WORKSPACE}/seed-deploy-$(date +%Y%m%d-%H%M%S).log"

# Parse args
for arg in "$@"; do
    case "$arg" in
        --commit) DRY_RUN=false ;;
        --push) DRY_RUN=false; DO_PUSH=true ;;
        --help|-h)
            echo "Usage: $0 [--commit] [--push]"
            echo "  (no args)  Dry-run: show what would be committed"
            echo "  --commit   Commit seed.yaml changes"
            echo "  --push     Commit and push to remote"
            exit 0
            ;;
        *) echo "Unknown arg: $arg"; exit 1 ;;
    esac
done

# Organ directories in deployment order
ORGANS=(
    "organvm-iv-taxis"
    "meta-organvm"
    "organvm-i-theoria"
    "organvm-ii-poiesis"
    "organvm-iii-ergon"
    "organvm-v-logos"
    "organvm-vi-koinonia"
    "organvm-vii-kerygma"
)

log() {
    local msg="[$(date +%H:%M:%S)] $1"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

log "Seed deployment started (dry_run=$DRY_RUN, push=$DO_PUSH)"
log "Log file: $LOG_FILE"
echo ""

total_committed=0
total_pushed=0
total_skipped=0
total_errors=0

for organ_dir in "${ORGANS[@]}"; do
    organ_path="${WORKSPACE}/${organ_dir}"
    if [[ ! -d "$organ_path" ]]; then
        log "SKIP: $organ_dir (directory not found)"
        continue
    fi

    log "=== Processing $organ_dir ==="

    for repo_dir in "$organ_path"/*/; do
        [[ -d "$repo_dir" ]] || continue
        repo_name="$(basename "$repo_dir")"
        seed_file="${repo_dir}seed.yaml"

        # Skip repos without seed.yaml
        if [[ ! -f "$seed_file" ]]; then
            continue
        fi

        # Skip if not a git repo
        if [[ ! -d "${repo_dir}.git" ]] && [[ ! -f "${repo_dir}.git" ]]; then
            continue
        fi

        # Check if seed.yaml has uncommitted changes
        if ! git -C "$repo_dir" diff --quiet -- seed.yaml 2>/dev/null && \
           ! git -C "$repo_dir" diff --cached --quiet -- seed.yaml 2>/dev/null; then
            # Has changes
            :
        elif git -C "$repo_dir" status --porcelain -- seed.yaml 2>/dev/null | grep -q .; then
            # Has changes (untracked or modified)
            :
        else
            # No changes to seed.yaml
            continue
        fi

        log "  ${organ_dir}/${repo_name}: seed.yaml modified"

        if "$DRY_RUN"; then
            git -C "$repo_dir" diff -- seed.yaml 2>/dev/null | head -20
            total_skipped=$((total_skipped + 1))
            continue
        fi

        # Commit
        if git -C "$repo_dir" add seed.yaml 2>/dev/null && \
           git -C "$repo_dir" commit -m "chore: reconcile seed.yaml (IGNITION)" 2>/dev/null; then
            log "    Committed"
            total_committed=$((total_committed + 1))
        else
            log "    ERROR: commit failed"
            total_errors=$((total_errors + 1))
            continue
        fi

        # Push
        if "$DO_PUSH"; then
            if git -C "$repo_dir" push 2>/dev/null; then
                log "    Pushed"
                total_pushed=$((total_pushed + 1))
            else
                log "    ERROR: push failed (may need to set upstream)"
                total_errors=$((total_errors + 1))
            fi
        fi
    done

    log ""
done

log "=== Summary ==="
log "Committed: $total_committed"
log "Pushed:    $total_pushed"
log "Skipped:   $total_skipped (dry-run)"
log "Errors:    $total_errors"
log "Log:       $LOG_FILE"

exit "$total_errors"
