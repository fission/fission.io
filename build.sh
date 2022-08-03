#!/bin/bash

set -euo pipefail

echo "Check submodule status"
git submodule update --init --recursive
git submodule status --recursive
git submodule foreach --recursive 'git status'

echo "Npm install"
npm install

echo "Running hugo"
hugo --minify --path-warnings --gc
