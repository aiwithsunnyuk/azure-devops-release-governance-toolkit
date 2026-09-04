#!/usr/bin/env bash
set -euo pipefail

TARGET_COMMIT="${1:-HEAD}"
PREV_TAG=$(git describe --tags --abbrev=0 "${TARGET_COMMIT}^" 2>/dev/null || git rev-list --max-parents=0 HEAD)
RELEASE_FILE="RELEASE_NOTES.md"

echo "### Release Summary (${BUILD_BUILDNUMBER:-Local})" > "$RELEASE_FILE"
echo "**Target Commit:** \`$TARGET_COMMIT\`" >> "$RELEASE_FILE"
echo "**Previous Release Marker:** \`$PREV_TAG\`" >> "$RELEASE_FILE"
echo "" >> "$RELEASE_FILE"
echo "#### Merged Changes" >> "$RELEASE_FILE"

git log "${PREV_TAG}..${TARGET_COMMIT}" --pretty=format:"* \%s ([\%h](https://dev.azure.com/organization/project/_git/repo/commit/\%H))" >> "$RELEASE_FILE"

echo "" >> "$RELEASE_FILE"
echo "Generated release notes written to $RELEASE_FILE"
