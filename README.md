# Leto

Leto is a browser for macOS that brings Arc's ideas to a fast, private,
open source Chromium base. It is built on top of
[Helium](https://github.com/imputnet/helium), and inherits Helium's privacy
defaults, ad blocking, and lightweight interface.

> [!NOTE]
> Leto is an early, independent project. It is not affiliated with or endorsed
> by Helium, imput, or The Browser Company. Arc is a trademark of The Browser
> Company.

## What Leto adds

- **Spaces.** Each profile is a Space, and all Spaces share one window. Switch
  with the Space bar at the bottom of the sidebar, a two-finger swipe on the
  sidebar, or Ctrl+Cmd+Left/Right. The "+" beside it adds a Space, and
  right-clicking a Space edits it.
- **A sidebar instead of a toolbar.** Back, forward, and reload sit next to the
  window controls, and a pill shows the current site. The page gets the whole
  window.
- **Command bar.** Cmd+T opens a floating search with history, open tabs, and
  suggestions. Cmd+L edits the current address.
- **Site controls.** Quick actions, your extensions, and site settings in one
  popover.
- **Downloads in the sidebar.** Downloads show at the bottom of the sidebar
  with their progress, and open in a popover beside it.
- **Automatic picture-in-picture.** A playing video follows you out when you
  switch tabs or Spaces, and returns when you come back.
- **Pinned tabs and archiving.** Cmd+D pins a tab, or drag it up into the
  pinned tabs; drag it back down to unpin it. Right-click a pinned tab to
  give it a name of its own. Drop tabs on a Space in the sidebar's footer to
  move them there. Tabs you haven't opened for 12 hours close into history
  on their own, which you can change in Settings.
- **Split view.** Cmd+Option+N asks what to open beside the current page, and
  Shift+Enter in the command bar opens any result in split view.
- **Link previews.** Shift-click a link to open it in a card over the page,
  then keep it as a tab, put it in split view, or dismiss it.
- **Links from other apps.** They open in a small window of their own, from
  which a page can move into a Space. Sites can be set to always open in a
  particular Space.
- **Reader view.** Cmd+Option+R shows just the article, with the system's
  fonts and light, sepia and dark themes.
- **Lighter and more private.** Tabs in Spaces you aren't using go to sleep,
  and Cmd+Shift+C copies links without tracking parameters.
- **Protected media plays.** Leto fetches Google's Widevine, which Helium
  leaves out, so Spotify and other DRM sites play.
- **Arc-like defaults.** Vertical tabs only, the last session restored on
  launch, appearance settings shared across Spaces, and emoji avatars for
  Spaces.

## How it's built

Leto is a fork of [helium-macos](https://github.com/imputnet/helium-macos),
Helium's macOS packaging and development tooling. Everything Leto changes lives
in [`patches/leto/`](patches/leto), applied after Helium's and
ungoogled-chromium's patches. Each patch is a single feature, so Leto can follow
new Helium releases by rebasing a small, readable patch set.

The logo lives in [`branding/`](branding).

## Building

See [docs/building.md](docs/building.md). Leto builds exactly like Helium:
`./build.sh` produces a release `.dmg`, and `source dev.sh` sets up the
development environment (`he setup`, `he build`, `he run`).

## Credits

### Helium
Leto would not exist without [Helium](https://github.com/imputnet/helium) by
[imput](https://github.com/imputnet). Helium's browser, its patches, and its
macOS tooling are the foundation that Leto's features are built on. If you
want a fast, private Chromium browser with a classic layout, use Helium.

### ungoogled-chromium
Helium, and so Leto, is based on
[ungoogled-chromium](https://github.com/ungoogled-software/ungoogled-chromium)
and [ungoogled-chromium-macos](https://github.com/ungoogled-software/ungoogled-chromium-macos).
Thanks to everyone behind ungoogled-chromium.

### Chromium
Leto is built from the [Chromium](https://www.chromium.org/) source code by
The Chromium Authors.

### Arc
Leto's interface is inspired by [Arc](https://arc.net/) by The Browser Company.

## License
Leto keeps Helium's license. All code, patches, modified portions of imported
code or patches, and any other content that is unique to Leto or Helium and not
imported from other repositories is licensed under GPL-3.0. See
[LICENSE](LICENSE).

Any content imported from other projects retains its original license (for
example, any original unmodified code imported from ungoogled-chromium remains
licensed under their [BSD 3-Clause license](LICENSE.ungoogled_chromium)).
