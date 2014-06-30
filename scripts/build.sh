#!/bin/bash
# Build script for Mac/Linux.

pyinstaller \
  --clean \
  --noconfirm \
  --onefile \
  --distpath ../dist \
  --workpath ../build \
  build.spec
