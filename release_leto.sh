#!/bin/bash
# Copyright 2026 The Leto Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.

# Makes a Leto release: builds it, packages the disk image, signs it for
# Sparkle with Leto's update key, and writes the update feed that copies of
# Leto check. With --publish, uploads both to a GitHub release, which every
# copy of Leto then offers as an update.
#
# Usage: ./release_leto.sh [--skip-build] [--publish] [--notes FILE]
#
# Needs Sparkle's tools (SPARKLE_BIN, by default ~/.leto-tools/sparkle/bin)
# and Leto's update key in the login keychain, made once with:
#   generate_keys --account leto
# Bump revision.txt before each release so its version is newer.

set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
src="$root/build/src"
sparkle_bin="${SPARKLE_BIN:-$HOME/.leto-tools/sparkle/bin}"
repo="Arjun-Ingole/leto"

build=1
publish=0
notes=""
while [ $# -gt 0 ]; do
  case "$1" in
    --skip-build) build=0 ;;
    --publish) publish=1 ;;
    --notes) notes="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

if [ "$build" = 1 ]; then
  (cd "$src" && env -u GOROOT -u GOBIN -u GOPATH \
    SISO_PATH="$src/third_party/siso/cipd/siso" \
    python3 third_party/depot_tools/autoninja.py -C out/Release chrome)
fi

app="$src/out/Release/Leto.app"
dmg="$("$root/package_leto.sh" "$app" | tail -1)"

plist="$app/Contents/Info.plist"
version="$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" "$plist")"
short_version="$(/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" "$plist")"
min_system="$(/usr/libexec/PlistBuddy -c "Print LSMinimumSystemVersion" "$plist")"
arch="arm64"
tag="v$short_version"
asset="Leto-$short_version-$arch.dmg"

release_dir="$root/build/release-$short_version"
rm -rf "$release_dir"
mkdir -p "$release_dir"
cp "$dmg" "$release_dir/$asset"

# Prints: sparkle:edSignature="..." length="..."
signature="$("$sparkle_bin/sign_update" --account leto "$release_dir/$asset")"

cat > "$release_dir/appcast-$arch.xml" <<EOF
<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0" xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle">
  <channel>
    <title>Leto</title>
    <item>
      <title>Leto $short_version</title>
      <pubDate>$(LC_ALL=C date -u "+%a, %d %b %Y %H:%M:%S +0000")</pubDate>
      <sparkle:version>$version</sparkle:version>
      <sparkle:shortVersionString>$short_version</sparkle:shortVersionString>
      <sparkle:minimumSystemVersion>$min_system</sparkle:minimumSystemVersion>
      <enclosure url="https://github.com/$repo/releases/download/$tag/$asset"
                 type="application/octet-stream" $signature />
    </item>
  </channel>
</rss>
EOF

echo "Release $short_version is ready in $release_dir"

if [ "$publish" = 1 ]; then
  notes_args=(--generate-notes)
  if [ -n "$notes" ]; then
    notes_args=(--notes-file "$notes")
  fi
  gh release create "$tag" --repo "$repo" --title "Leto $short_version" \
    "${notes_args[@]}" \
    "$release_dir/$asset" "$release_dir/appcast-$arch.xml"
fi
