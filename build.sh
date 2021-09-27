#!/bin/bash

set -euo pipefail

echo "Check submodule status"
git submodule update --init --recursive
git submodule status --recursive
git submodule foreach --recursive 'git status'

echo "Npm install"
# npm install -D --save autoprefixer postcss-cli postcss
npm install -D --save autoprefixer@9.7.6 postcss-cli@7.1.0

echo "Running hugo"
hugo
