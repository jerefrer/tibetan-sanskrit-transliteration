#!/bin/bash

# Exit on error
set -e

echo "🔄 Publishing tibetan-sanskrit-transliteration..."

# Check if version argument is provided
if [ -z "$1" ]; then
    echo "❌ Error: Version argument required"
    echo "Usage: ./publish.sh <version>"
    echo "Example: ./publish.sh 0.1.3"
    exit 1
fi

NEW_VERSION=$1

# Validate version format (basic check)
if ! [[ $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "❌ Error: Invalid version format. Use semantic versioning (e.g., 0.1.3)"
    exit 1
fi

echo "📝 Bumping version to $NEW_VERSION..."

# Update version in pyproject.toml
sed -i '' "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Update version in __init__.py
sed -i '' "s/^__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" tibetan_sanskrit_transliteration/__init__.py

echo "✅ Version bumped to $NEW_VERSION"

# Clean dist directory
echo "🧹 Cleaning dist directory..."
rm -rf dist/
rm -rf build/
rm -rf *.egg-info

# Run tests
echo "🧪 Running tests..."
python3 -m pytest tests/ -v

# Build package
echo "📦 Building package..."
python3 -m build

# Publish to PyPI
echo "🚀 Publishing to PyPI..."
python3 -m twine upload dist/*

echo "✅ Successfully published version $NEW_VERSION to PyPI!"
echo "📝 Don't forget to commit and push the version changes:"
echo "   git add pyproject.toml tibetan_sanskrit_transliteration/__init__.py"
echo "   git commit -m \"Bump version to $NEW_VERSION\""
echo "   git push"
