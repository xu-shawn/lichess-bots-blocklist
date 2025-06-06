#!/usr/bin/env bash

cat blocklist | sort -u -o blocklist
cat whitelist | sort -u -o whitelist
