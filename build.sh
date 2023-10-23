#!/bin/bash

set -euo pipefail

echo "Npm install"
npm install

echo "Running hugo"
hugo --minify --printPathWarnings --gc
