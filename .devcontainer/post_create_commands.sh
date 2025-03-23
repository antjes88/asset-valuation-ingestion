#!/bin/bash
# shellcheck disable=SC1091,SC2059

chmod +x /workspaces/csv-ingestion/cli/bin/csv-ingestion
git config --global --add safe.directory /workspaces/csv-ingestion
gcloud auth application-default login
