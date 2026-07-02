#!/usr/bin/env bash

cat blocklist | sort -f -u -o blocklist
cat whitelist | sort -f -u -o whitelist
