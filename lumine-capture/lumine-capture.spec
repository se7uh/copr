%global debug_package %{nil}
%global rust_toolchain rust >= 1.88.0

Name:           lumine-capture
Version:        0.2.0
Release:        1%{?dist}
Summary:        Screenshot and annotation tool for Wayland with built-in OCR

License:        (MIT OR Apache-2.0) AND OFL-1.1
URL:            https://github.com/Netflate/LumineCapture
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang
BuildRequires:  clang-devel
BuildRequires:  %{rust_toolchain}
BuildRequires:  cargo
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
cargo build --release %{?_smp_flags}

%install
# Main binary
install -D -p -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Desktop entry
install -D -p -m 0644 assets/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

# Icons
for icon in assets/hicolor/*/apps/*; do
    install -D -p -m 0644 "$icon" "%{buildroot}%{_datadir}/icons/${icon#assets/}"
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
cargo test --release || :

%files
%license LICENSE-MIT LICENSE-APACHE assets/fonts/LICENSE-OFL.txt
%doc README.md docs/lumine-capture-shortcuts-kde.kksrc
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/lumine-capture.*
%{_datadir}/icons/hicolor/*/apps/lumine-pin.*

%changelog
* Tue Oct 13 2026 boobaa <xenialv7@gmail.com> - 0.2.0-1
- Initial package for Fedora COPR
