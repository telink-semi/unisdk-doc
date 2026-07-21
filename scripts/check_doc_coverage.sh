#!/bin/bash
# check_doc_coverage.sh
#
# Verify that all .md/.rst documentation files under source/ are listed
# in a toctree inside source/index.rst.
#
# Usage: ./scripts/check_doc_coverage.sh
# Exit code: 0 if all files are covered, 1 if any are missing.

set -euo pipefail

DOC_DIR="source"
INDEX_RST="$DOC_DIR/index.rst"

# Patterns to exclude from coverage checking
EXCLUDE_PATTERNS=(
  '-not -path "*/pics/*"'
  '-not -path "*/api_reference/*"'
  '-not -path "*_build/*"'
)

echo "=== Checking toctree coverage in $INDEX_RST ==="

# Build find expression
FIND_EXPR="find \"$DOC_DIR\" -type f \( -name '*.md' -o -name '*.rst' \)"
for pat in "${EXCLUDE_PATTERNS[@]}"; do
  FIND_EXPR="$FIND_EXPR $pat"
done

# Collect all doc files into a temp file
TEMP_FILE=$(mktemp)
eval "$FIND_EXPR" | sort > "$TEMP_FILE"

MISSING=0
while IFS= read -r filepath; do
  # Strip source/ prefix and extension
  entry="${filepath#$DOC_DIR/}"
  entry="${entry%.md}"
  entry="${entry%.rst}"

  # Skip source/index.rst itself
  if [ "$entry" = "index" ]; then
    continue
  fi

  # Check if this entry appears in index.rst (as toctree entry)
  if ! grep -Fq "$entry" "$INDEX_RST"; then
    echo "MISSING: $entry  ($filepath)"
    MISSING=$((MISSING + 1))
  fi
done < "$TEMP_FILE"

rm -f "$TEMP_FILE"

if [ $MISSING -gt 0 ]; then
  echo ""
  echo "FAILED: $MISSING file(s) are not listed in any toctree in $INDEX_RST."
  echo "Either add them to the appropriate toctree in $INDEX_RST,"
  echo "or add an exclusion pattern to the script if intentionally excluded."
  exit 1
else
  echo "OK: All documentation files are covered by toctree entries."
  exit 0
fi
