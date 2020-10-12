#!/usr/bin/env bash

# Abort this script when undefined variable used
set -u

# Abort this script when command fails
set -e

# Get absolute directory path where this script exists
SCRIPT_DIR="$(cd $(dirname "${BASH_SOURCE:-$0}"); pwd)"

# Change working directory
pushd "${SCRIPT_DIR}" > /dev/null

# Load $STAGE from .env file
if [[ ! -e ".env" ]]; then
  echo "[ERROR] .env file not found." >&2
  exit 1
fi
source ".env"

echo "[INFO] Building Dockerfiles..."
docker-compose -f "docker-compose-${STAGE}.yml" up --build -d

# Back to previous directory
popd > /dev/null
