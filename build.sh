#!/bin/bash

set -euo pipefail

echo "Npm install"
npm install

echo "Running hugo"
# Deploy previews and branch deploys must emit their own domain in absolute
# URLs (ref shortcodes), otherwise preview links jump to fission.io.
if [ "${CONTEXT:-production}" != "production" ] && [ -n "${DEPLOY_PRIME_URL:-}" ]; then
  hugo --minify --printPathWarnings --gc -b "$DEPLOY_PRIME_URL"
else
  hugo --minify --printPathWarnings --gc
fi
