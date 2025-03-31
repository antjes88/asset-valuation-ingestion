#!/bin/bash
# shellcheck disable=SC1091,SC2059

sed -i 's/\r$//' /workspaces/asset-valuation-ingestion/cli/bin/asset-valuation-ingestion
chmod +x /workspaces/asset-valuation-ingestion/cli/bin/asset-valuation-ingestion
git config --global --add safe.directory /workspaces/asset-valuation-ingestion
gcloud auth application-default login

FILE="./.devcontainer/git_config.sh"
if [ -f "$FILE" ]; then
    chmod +x "$FILE"
    "$FILE"
else
    echo "$FILE not found. Follow instructions in README.md to set up git config. ### Configure Git"
fi