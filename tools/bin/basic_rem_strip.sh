#!/usr/bin/env bash
# basic_rem_strip.sh
# Usage:
#   basic_rem_strip.sh < input.bas > output.bas
#   basic_rem_strip.sh input.bas > output.bas

awk '
function ltrim(s) { sub(/^[[:space:]]+/, "", s); return s }
function rtrim(s) { sub(/[[:space:]]+$/, "", s); return s }

{
    orig = $0

    # Strip lines that are empty or only whitespace
    if (orig ~ /^[[:space:]]*$/) {
        next
    }

    line = orig

    # Match: optional spaces, line number, optional spaces
    if (!match(line, /^[[:space:]]*[0-9]+[[:space:]]*/)) {
        # Not a numbered BASIC line; pass through unchanged
        print orig
        next
    }

    # Extract prefix (spaces + number + spaces), then boil it down to just the number
    prefix = substr(line, RSTART, RLENGTH)
    ln = prefix
    ln = ltrim(ln)
    ln = rtrim(ln)

    # Everything after prefix is BASIC body
    body = substr(line, RSTART + RLENGTH)

    # --- Drop lines that are only REM after the line number ---
    temp = ltrim(body)
    up   = toupper(temp)
    if (up ~ /^REM([[:space:]]|$)/) {
        next
    }

    # --- Strip a trailing REM-only statement (2nd, 3rd, etc.) ---
    # Find the FIRST ":" outside of strings such that the tail starts with REM.
    in_string = 0
    cutPos    = 0
    len = length(body)

    for (i = 1; i <= len; i++) {
        c = substr(body, i, 1)

        if (!in_string && c == "\"") {
            in_string = 1
        } else if (in_string && c == "\"") {
            # Handle doubled quotes "" inside strings
            if (i < len && substr(body, i+1, 1) == "\"") {
                i++    # skip escaped quote, stay inside string
            } else {
                in_string = 0
            }
        } else if (!in_string && c == ":") {
            tail      = substr(body, i + 1)
            tail_trim = ltrim(tail)
            tail_up   = toupper(tail_trim)

            if (tail_up ~ /^REM([[:space:]]|$)/) {
                cutPos = i
                break
            }
        }
    }

    if (cutPos > 0) {
        body = substr(body, 1, cutPos - 1)
        body = rtrim(body)
    }

    # Remove indentation immediately after the line number
    body = ltrim(body)

    # If nothing left after stripping comments and trimming, drop the line
    if (length(body) == 0) {
        next
    }

    print ln " " body
}
' "$@"
