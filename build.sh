#!/bin/bash

set -euo pipefail

npm install -D --save autoprefixer postcss-cli

echo "Running hugo"
hugo
