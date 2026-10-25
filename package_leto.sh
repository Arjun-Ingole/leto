#!/bin/bash
# Copyright 2026 The Leto Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.

# Signs Leto ad hoc and packages it as its installer disk image, with the
# window laid out by resources/leto/dmg.
#
# Usage: ./package_leto.sh [path/to/Leto.app]
# Defaults to the release build in build/src/out/Release.

set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
app="${1:-$root/build/src/out/Release/Leto.app}"
venv="$root/build/.dmg-venv"

if [ ! -x "$venv/bin/dmgbuild" ]; then
  python3 -m venv "$venv"
  "$venv/bin/pip" install --quiet dmgbuild
fi

codesign --force --deep --sign - "$app"
codesign --verify --deep --strict "$app"

chromium_version="$(cat "$root/helium-chromium/chromium_version.txt")"
helium_revision="$(cat "$root/helium-chromium/revision.txt")"
platform_revision="$(cat "$root/revision.txt")"
out="$root/build/leto_${chromium_version}-${helium_revision}.${platform_revision}_macos.dmg"

rm -f "$out"
"$venv/bin/dmgbuild" -s "$root/resources/leto/dmg/dmg_settings.py" \
  -D app="$app" -D resources="$root/resources/leto/dmg" Leto "$out"
hdiutil verify "$out" >/dev/null
echo "$out"
