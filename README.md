# My COPR Repository

Spec files I maintain on [Fedora COPR](https://copr.fedorainfracloud.org/coprs/boobaa/).

All of these are tools I use daily, so they get updated and tested as I use them.

A [GitHub Action](.github/workflows/check-upstream-versions.yml) checks for new
upstream releases daily and opens an issue when something is outdated.

## Packages

| Package | Description | Version | Upstream | COPR |
|---------|-------------|---------|----------|------|
| bustd   | Lightweight OOM-killer daemon | 0.1.1 | [vrmiguel/bustd](https://github.com/vrmiguel/bustd) | [boobaa/bustd](https://copr.fedorainfracloud.org/coprs/boobaa/bustd/) |
| git-id  | Git account switcher | 1.1.2 | [se7uh/git-id](https://github.com/se7uh/git-id) | [boobaa/git-id](https://copr.fedorainfracloud.org/coprs/boobaa/git-id/) |
| ouch    | Painless compression in the terminal | 0.8.1 | [ouch-org/ouch](https://github.com/ouch-org/ouch) | [boobaa/ouch](https://copr.fedorainfracloud.org/coprs/boobaa/ouch/) |
| yazi    | Blazing fast terminal file manager | 26.5.6 | [sxyazi/yazi](https://github.com/sxyazi/yazi) | [boobaa/yazi](https://copr.fedorainfracloud.org/coprs/boobaa/yazi/) |
| zellij  | A terminal workspace with batteries included | 0.44.3 | [zellij-org/zellij](https://github.com/zellij-org/zellij) | [boobaa/zellij](https://copr.fedorainfracloud.org/coprs/boobaa/zellij/) |

```bash
sudo dnf copr enable boobaa/<package>
sudo dnf install <package>
```
