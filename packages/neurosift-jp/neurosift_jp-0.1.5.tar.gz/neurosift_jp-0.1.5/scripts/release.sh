#!/bin/bash

# Prompt for new version
echo "Enter new version:"
read VERSION

# Bump version using hatch
echo "Bumping version to $VERSION..."
hatch version $VERSION

# Clean up
echo "Cleaning..."
jlpm clean:all
if [ -d "dist" ]; then
    echo "Removing dist directory..."
    rm -rf dist
fi

# Build
echo "Building package..."
python -m build

# Ask about upload
echo "Upload to PyPI? (y/N):"
read UPLOAD

if [ "$UPLOAD" = "y" ] || [ "$UPLOAD" = "Y" ]; then
    echo "Uploading to PyPI..."
    twine upload dist/*
fi

echo "Done!"
