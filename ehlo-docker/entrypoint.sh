#!/bin/sh

# Use provided TARGET_URL or default fallback
: "${TARGET_URL:=http://localhost/myAwesomApi}"

ehlo -p 10025 -a "$TARGET_URL"