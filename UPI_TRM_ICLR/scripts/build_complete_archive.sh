#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$SOURCE_ROOT/.." && pwd)"
MANIFEST="$SOURCE_ROOT/review/ICLR_BUNDLE_FILE_LIST.txt"
OUTPUT_ZIP="${UPI_TRM_ICLR_ARCHIVE_OUTPUT:-$REPO_ROOT/UPI_TRM_ICLR_COMPLETE.zip}"
OUTPUT_SHA="$OUTPUT_ZIP.sha256"
TEMP_ROOT="$(mktemp -d)"
STAGED_ROOT="$TEMP_ROOT/UPI_TRM_ICLR"
TEMP_ZIP="$TEMP_ROOT/UPI_TRM_ICLR_COMPLETE.zip"
HOME_PATH_PATTERN='/(home)/'
MAC_USER_PATH_PATTERN='/User(s)/'
DATA_USER_PATH_PATTERN='/data/user(s)/'
PRIOR_TREE_PATTERN='UPI_TRM_N[A-Z]+'
PRIOR_VENUE_PATTERN='N(eur)IPS'
LOWER_PRIOR_VENUE_PATTERN='n(eur)ips'
SHORT_VENUE_PATTERN='NIP(S)'
LOWER_SHORT_VENUE_PATTERN='nip(s)'
LEGACY_USER_PATTERN='buik(sat)'
FORBIDDEN_PATTERN="$HOME_PATH_PATTERN|$MAC_USER_PATH_PATTERN|$DATA_USER_PATH_PATTERN|$PRIOR_TREE_PATTERN|$PRIOR_VENUE_PATTERN|$LOWER_PRIOR_VENUE_PATTERN|$SHORT_VENUE_PATTERN|$LOWER_SHORT_VENUE_PATTERN|$LEGACY_USER_PATTERN"

cleanup() {
    rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

mkdir -p -- "$STAGED_ROOT"

while IFS= read -r relative_path; do
    [[ -n "$relative_path" ]] || continue
    [[ "$relative_path" != /* && "$relative_path" != *".."* ]] || {
        printf 'Unsafe archive path: %s\n' "$relative_path" >&2
        exit 1
    }
    source_path="$SOURCE_ROOT/$relative_path"
    [[ -e "$source_path" || -L "$source_path" ]] || {
        printf 'Missing required archive input: %s\n' "$relative_path" >&2
        exit 1
    }
    mkdir -p -- "$STAGED_ROOT/$(dirname "$relative_path")"
    cp -a -- "$source_path" "$STAGED_ROOT/$relative_path"
done < "$MANIFEST"

# Historical evidence retains its semantics, but local usernames, absolute home
# paths, and prior-venue labels do not belong in a double-blind archive.
while IFS= read -r -d '' staged_file; do
    if [[ ! -s "$staged_file" ]] || grep -Iq . "$staged_file"; then
        perl -pi -e 's{/(?:home)/[A-Za-z0-9._-]+/trm_bellman}{<CODE_REPO_ROOT>}g; s{/(?:home)/[A-Za-z0-9._-]+/UPI_TRM/UPI_TRM_N[A-Z]+}{<HISTORICAL_PAPER_ROOT>}g; s{/(?:home)/[A-Za-z0-9._-]+/UPI_TRM/UPI_TRM_ICLR}{<PAPER_SOURCE_ROOT>}g; s{/data/(?:users)/[A-Za-z0-9._-]+/fbsource(?:/fbcode)?}{<BUILD_ROOT>}g; s{/(?:home)/[A-Za-z0-9._-]+}{<ANON_HOME>}g; s{/(?:Users)/[A-Za-z0-9._-]+}{<ANON_HOME>}g; s{UPI_TRM_N[A-Z]+}{HISTORICAL_PAPER_TREE}g; s{N(?:eur)IPS}{prior venue}g; s{n(?:eur)ips}{prior_venue}g; s{NIP(?:S)}{LEGACY}g; s{nip(?:s)}{legacy}g; s{buik(?:sat)}{anon}ig' "$staged_file"
    fi
done < <(find "$STAGED_ROOT" -type f -print0)

if find "$STAGED_ROOT" -print | grep -Eq "$FORBIDDEN_PATTERN"; then
    printf 'Archive filename anonymization check failed.\n' >&2
    exit 1
fi

if rg -a -l --hidden --no-ignore "$FORBIDDEN_PATTERN" "$STAGED_ROOT"; then
    printf 'Archive content anonymization check failed.\n' >&2
    exit 1
fi

(
    cd "$TEMP_ROOT"
    find UPI_TRM_ICLR -type f ! -name SHA256SUMS -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > UPI_TRM_ICLR/SHA256SUMS
    find UPI_TRM_ICLR -type f -exec touch -t 198001010000.00 {} +
    find UPI_TRM_ICLR -type f -print | LC_ALL=C sort | zip -X -q "$TEMP_ZIP" -@
)

mkdir -p -- "$(dirname "$OUTPUT_ZIP")"
mv -f -- "$TEMP_ZIP" "$OUTPUT_ZIP"
(
    cd "$(dirname "$OUTPUT_ZIP")"
    sha256sum "$(basename "$OUTPUT_ZIP")" > "$(basename "$OUTPUT_SHA")"
)

printf 'Wrote %s\n' "$OUTPUT_ZIP"
printf 'Wrote %s\n' "$OUTPUT_SHA"
