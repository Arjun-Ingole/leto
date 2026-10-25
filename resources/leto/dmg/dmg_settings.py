# Copyright 2026 The Leto Authors
# You can use, redistribute, and/or modify this source code under
# the terms of the GPL-3.0 license that can be found in the LICENSE file.

# dmgbuild settings for Leto's installer: Leto on the left, Applications on
# the right, over the background drawn by make_background.py.
#
# Usage: dmgbuild -s dmg_settings.py -D app=/path/to/Leto.app \
#            -D resources=/path/to/this/folder Leto out.dmg

import os.path

_here = defines["resources"]  # noqa: F821
_app = defines["app"]  # noqa: F821
_name = os.path.basename(_app)

format = "ULMO"
filesystem = "APFS"
files = [_app]
symlinks = {"Applications": "/Applications"}
icon = os.path.join(_app, "Contents", "Resources", "app.icns")
# dmgbuild picks up background@2x.png for Retina screens.
background = os.path.join(_here, "background.png")

# Keep in step with make_background.py.
window_rect = ((200, 120), (660, 400))
icon_size = 112
text_size = 13
icon_locations = {
    _name: (170, 150),
    "Applications": (490, 150),
}
show_status_bar = False
show_tab_view = False
show_toolbar = False
show_pathbar = False
show_sidebar = False
default_view = "icon-view"
show_icon_preview = False
include_icon_view_settings = True
arrange_by = None
label_pos = "bottom"
