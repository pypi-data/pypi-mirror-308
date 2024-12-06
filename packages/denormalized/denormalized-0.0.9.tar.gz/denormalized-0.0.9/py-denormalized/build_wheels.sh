#!/bin/bash
set -euo pipefail

echo "🔨 Building macOS universal2 wheel..."
maturin build --zig --release --target universal2-apple-darwin

echo "🐋 Building Linux wheels using Zig..."
# docker run --rm -v $(pwd):/io ghcr.io/pyo3/maturin build --release --zig
maturin build --zig --release --target x86_64-unknown-linux-gnu
maturin build --zig --release --target aarch64-unknown-linux-gnu


echo "🎯 Building source distribution..."
maturin sdist

echo "⬆️  Uploading all distributions to PyPI..."
# maturin upload target/wheels/*.whl
# maturin upload target/wheels/*.tar.gz

echo "✅ Done! Wheels and sdist have been uploaded to PyPI"
