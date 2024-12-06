#!/usr/bin/env bash

set -e
set -x

echo "Running ruff check..."
uv run ruff check zendriver
echo "Running ruff format check..."
uv run ruff format zendriver --check
echo "Running mypy..."
uv run mypy zendriver
