#!/bin/bash

# Exit on error
set -e

echo "🔄 Publishing tibetan-sanskrit-transliteration..."

# Check if bump type argument is provided
if [ -z "$1" ]; then
    echo "❌ Error: Version bump type required"
    echo "Usage: ./publish.sh <major|minor|patch>"
    echo "Example: ./publish.sh patch"
    exit 1
fi

BUMP_TYPE=$1

# Validate bump type
if [[ ! "$BUMP_TYPE" =~ ^(major|minor|patch)$ ]]; then
    echo "❌ Error: Invalid bump type. Use 'major', 'minor', or 'patch'"
    exit 1
fi

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')

# Parse version components
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT_VERSION"

# Bump version based on type
case $BUMP_TYPE in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"

echo "📝 Bumping version from $CURRENT_VERSION to $NEW_VERSION ($BUMP_TYPE)..."

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
