#!/bin/bash

set -euo pipefail

echo "Running hugo"
hugo --minify --printPathWarnings --gc
