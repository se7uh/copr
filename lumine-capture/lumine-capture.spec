%global debug_package %{nil}

Name:           lumine-capture
Version:        0.3.0
Release:        1%{?dist}
Summary:        Screenshot and annotation tool for Wayland with built-in OCR

License:        (MIT OR Apache-2.0) AND MIT AND OFL-1.1
URL:            https://github.com/Netflate/LumineCapture
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# ONNX Runtime ships prebuilt only for these
ExclusiveArch:  x86_64 aarch64

BuildRequires:  rust >= 1.88
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  clang-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pipewire-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  openssl-devel
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme

%description
LumineCapture is a fast, lightweight Wayland screenshot and annotation tool
written in Rust with built-in OCR.

Features:
- Fast startup and capturing without requiring a background daemon
- Multi-backend capture: KWin ScreenShot2, ext-image-copy-capture,
  wlr-screencopy, or XDG Desktop Portal
- In-app screenshot editing and annotation (shapes, arrows, text, blur, pixelate)
- Built-in offline OCR (PaddleOCR PP-OCRv5 via ONNX Runtime)
- Pin screenshots to screen
- Configurable keyboard shortcuts and output actions

%prep
%autosetup -n LumineCapture-%{version}

%build
# Fedora's RUSTFLAGS turn strip off and add debuginfo, overriding profile.dist
unset RUSTFLAGS
# the build script downloads the ONNX Runtime it links against
cargo build --locked --profile dist

%install
# Main binary (KWin grants screenshot access by the Exec= path, so /usr/bin/lumine-capture)
install -D -p -m 0755 target/dist/%{name} %{buildroot}%{_bindir}/%{name}

# Desktop entry
install -D -p -m 0644 assets/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons
for icon in assets/hicolor/*/apps/*; do
    install -D -p -m 0644 "$icon" "%{buildroot}%{_datadir}/icons/${icon#assets/}"
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
unset RUSTFLAGS
cargo test --locked --profile dist || :

%files
%license LICENSE-MIT LICENSE-APACHE assets/fonts/LICENSE-OFL.txt
%doc README.md docs/lumine-capture-shortcuts-kde.kksrc
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/lumine-capture.*
%{_datadir}/icons/hicolor/*/apps/lumine-pin.*

%changelog
* Mon Oct 19 2026 boobaa <xenialv7@gmail.com> - 0.3.0-1
- Update to 0.3.0
- Add blur and pixelate redact tool and highlighter tool
- Support Shift snapping to straight lines and text outline
- Add delay and nonotify flags, and improved OCR options
- Show screenshot preview in notifications when copying or pinning

* Tue Oct 13 2026 boobaa <xenialv7@gmail.com> - 0.2.0-1
- Initial package for Fedora COPR
