# Zen Browser — COPR Package

[Zen Browser](https://zen-browser.app/) is a Firefox-based browser focused on
simplicity, performance, and privacy. It brings features like workspace
management, vertical tabs, and split view — giving you a calmer, more
organised web experience.

This directory contains the RPM spec files to package Zen Browser for
Fedora/RHEL via [COPR](https://copr.fedorainfracloud.org/).

## Why This Package?

The official Zen Browser releases only provide tarballs (`.tar.xz`) and
AppImages. This spec wraps the pre-built upstream tarball into a proper RPM,
giving you:

- System-wide installation managed by DNF
- Desktop entry and icon integration
- Wayland support out of the box
- Automatic updates via your package manager

## Credits

This spec is based on the excellent work by
**[SnenxyTengoku](https://github.com/SnenxyTengoku)** ([GitHub](https://github.com/SnenxyTengoku/copr)),
who maintains the `sneexy/zen-browser` COPR repository. Their original spec and
packaging files for Zen Browser and Floorp were the foundation for this
package. Huge thanks for their contributions to the Fedora/COPR ecosystem!

This version was independently maintained to give users an additional trusted
source. The packaging approach (wrapper script, `.desktop` file, policy config)
follows the same pattern established by their work.

Other references used:
- [the4runner](https://github.com/the4runner/firefox-dev) — Firefox Developer
  Edition packaging reference
- [AUR PKGBUILD](https://aur.archlinux.org/packages/zen-browser-bin) — Arch
  Linux packaging reference

## Installation

```bash
# Enable the COPR repository
sudo dnf copr enable boobaa/zen-browser

# Install Zen Browser
sudo dnf install zen-browser

# Launch
zen-browser
```

## Package Contents

| File | Purpose |
|------|---------|
| `zen-browser.spec` | RPM spec file for x86_64 and aarch64 |
| `zen-browser` | Launcher wrapper (Wayland + DE integration) |
| `zen-browser.desktop` | Desktop entry for application menus |
| `policies.json` | Firefox policy (disables built-in updates) |

## Notes

- This package downloads the **official pre-built binary** from GitHub Releases.
  No code modifications are made.
- Built-in update checks are disabled via `policies.json` — updates are handled
  through DNF/COPR instead.
- No Twilight (nightly) package here
