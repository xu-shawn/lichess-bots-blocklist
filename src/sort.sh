#!/usr/bin/env bash

filename="${1:-blocklist}"
cat "$filename" | sort -u -o "$filename"
