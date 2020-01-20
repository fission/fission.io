#!/bin/bash

set -euo pipefail

cd docs
npm install -D --save autoprefixer postcss-cli

echo "Running hugo"
hugo
