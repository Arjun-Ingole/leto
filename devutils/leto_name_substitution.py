#!/usr/bin/env python3

# Copyright 2026 The Leto Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.
"""Runs Helium's name substitution, naming the browser Leto instead.

Helium replaces Chrome and Chromium with Helium in Chromium's user-facing
strings. Leto reuses that machinery (including the backup and restore used by
`he namesub` and `he nameunsub`) and swaps in its own replacements: Chrome,
Chromium and Helium all become Leto. Internal helium:// URLs are left as they
are, since the scheme is wired into Helium's code.

Takes the same arguments as helium-chromium/utils/name_substitution.py.
"""

import re
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / 'helium-chromium' / 'utils'))

# pylint: disable=wrong-import-position
import name_substitution  # noqa: E402
import name_substitution_utils as util  # noqa: E402

# This runs at import time so that worker processes, which import this module
# afresh, use Leto's replacements too.
util.REPLACEMENT_REGEXES = [(re.compile(pattern), replacement)
                            for pattern, replacement in [
                                # stuff we don't want to replace
                                (r'(\w+) Root Program', r'\1_unreplace Root Program'),
                                (r'(\w+) Web( S|s)tore', r'\1_unreplace Web Store'),
                                (r'(\w+) Remote Desktop', r'\1_unreplace Remote Desktop'),

                                # main replacement(s)
                                (r'(\b)chrome://', r'\1helium://'),
                                (r'(?:Google )?Chrom(e|ium)(?!\w)', r'Leto'),
                                (r'(?<![\w/])Helium(?!\w)', r'Leto'),

                                # post-replacement cleanup
                                (r'((?:Google )?Chrom(e|ium))_unreplace', r'\1'),
                                (r'_unreplace', r''),
                            ]]


_replace_grit_tree = util.replace_grit_tree


def replace_grit_tree(text):
    """Like Helium's, but keeps files without an XML declaration that way.

    Rewriting a file adds a declaration, which tools that read .grdp files
    directly, like Helium's onboarding string generator, don't expect."""
    replaced, fp_map = _replace_grit_tree(text)
    if fp_map and not text.lstrip().startswith('<?xml') and replaced.startswith('<?xml'):
        replaced = replaced.split('\n', 1)[1] if '\n' in replaced else ''
    return replaced, fp_map


util.replace_grit_tree = replace_grit_tree


def replacement_sanity():
    """Checks that the replacements behave as intended"""
    before_after = [
        ('chrome://about', 'helium://about'),
        ('Chrome Root Program', 'Chrome Root Program'),
        (' Chrome  ', ' Leto  '),
        ('Chrome Web Store', 'Chrome Web Store'),
        ('Google Chrome', 'Leto'),
        ('Chromium', 'Leto'),
        ('Welcome to Helium', 'Welcome to Leto'),
        ('Helium Setup', 'Leto Setup'),
    ]

    for source, expected in before_after:
        modified, match = util.replace_text(source)
        assert match, f"sanity: {expected} should have a match"
        assert modified == expected, f"sanity: {modified} != {expected}"


name_substitution.replacement_sanity = replacement_sanity

if __name__ == '__main__':
    name_substitution.main()
