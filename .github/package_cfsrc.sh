#!/bin/bash
set -e

if [[ $# -lt 2 ]]; then
    echo "❌ Error: Missing parameters!"
    echo "Usage: $0 <RUNNER_TEMP> <OUTPUT_FILE_PATH>"
    exit 1 
fi

# Assign parameters
RUNNER_TEMP="$1"
OUTPUT_FILE_PATH="$2"

rm -rf "$RUNNER_TEMP/cloud_function"
mkdir -p "$RUNNER_TEMP/cloud_function"

cp -r "./src/entrypoints/cloud_function/main.py" "$RUNNER_TEMP/cloud_function/"
cp -r ./src "$RUNNER_TEMP/cloud_function/"
cp -r "./requirements.txt" "$RUNNER_TEMP/cloud_function/"

rm -rf "$RUNNER_TEMP/cloud_function/src/entrypoints"
rm -rf "$RUNNER_TEMP/cloud_function/src/__pycache__"

echo "Packaging src code for cloud function..."
find "$RUNNER_TEMP/cloud_function" -type f

cd "$RUNNER_TEMP/cloud_function"
zip -r "$OUTPUT_FILE_PATH" .
cd ../..

echo "Cloud function code packaged successfully at $OUTPUT_FILE_PATH"
echo "removing temp files..."
rm -rf "$RUNNER_TEMP/cloud_function"