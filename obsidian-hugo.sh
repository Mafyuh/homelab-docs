#!/bin/bash

# Set variables for Obsidian to Hugo copy
SOURCE_PATH="/home/mafyuh/Documents/Obsidian Vault/iac-docs/docs"
DESTINATION_PATH="/home/mafyuh/homelab-docs/content/docs"
MY_REPO="git@github.com:mafyuh/homelab-docs.git"

# Error handling
set -euo pipefail

# Change to the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check for required commands
REQUIRED_COMMANDS=("git" "python3")
for CMD in "${REQUIRED_COMMANDS[@]}"; do
    if ! command -v "$CMD" &>/dev/null; then
        echo "Error: $CMD is not installed or not in PATH." >&2
        exit 1
    fi
done

# Step 1: Check if Git is initialized, and initialize if necessary
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git remote add origin "$MY_REPO"
else
    echo "Git repository already initialized."
    if ! git remote | grep -q "origin"; then
        echo "Adding remote origin..."
        git remote add origin "$MY_REPO"
    fi
fi

# Step 2: Sync posts from Obsidian to Hugo content folder using rsync
echo "Syncing posts from Obsidian..."

if [ ! -d "$SOURCE_PATH" ]; then
    echo "Error: Source path does not exist: $SOURCE_PATH" >&2
    exit 1
fi

if [ ! -d "$DESTINATION_PATH" ]; then
    echo "Error: Destination path does not exist: $DESTINATION_PATH" >&2
    exit 1
fi

rsync -av --delete "$SOURCE_PATH/" "$DESTINATION_PATH/"

# Step 3: Process Markdown files with Python script to handle image links
echo "Processing image links in Markdown files..."
if [ ! -f "linux-images.py" ]; then
    echo "Error: Python script images.py not found." >&2
    exit 1
fi

python3 linux-images.py

# Step 4: Add changes to Git
echo "Staging changes for Git..."
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to stage."
else
    git add .
fi

# Step 5: Commit changes with a dynamic message
COMMIT_MESSAGE="New Blog Post on $(date '+%Y-%m-%d %H:%M:%S')"
if [ -z "$(git diff --cached --name-only)" ]; then
    echo "No changes to commit."
else
    echo "Committing changes..."
    git commit -m "$COMMIT_MESSAGE"
fi

# Step 6: Push all changes to the main branch
echo "Deploying to GitHub Main..."
if ! git push origin main; then
    echo "Error: Failed to push to GitHub." >&2
    exit 1
fi

echo "All done! Site synced, processed, committed, built, and deployed."
