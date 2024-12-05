#!/bin/sh -e
set -x

uv run ruff check zendriver --fix
uv run ruff format zendriver
