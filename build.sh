#!/bin/bash

set -euo pipefail

# npm install -D --save autoprefixer postcss-cli postcss
npm install -D --save autoprefixer@9.7.6 postcss-cli@7.1.0

echo "Running hugo"
hugo
