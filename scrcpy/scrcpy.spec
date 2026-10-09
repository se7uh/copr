%global debug_package %{nil}

Name:           scrcpy
Version:        5.0.1
Release:        1%{?dist}
Summary:        Display and control your Android device

License:        Apache-2.0
URL:            https://github.com/Genymobile/scrcpy
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/scrcpy-server-v%{version}

BuildRequires:  gcc
BuildRequires:  meson >= 0.49
BuildRequires:  ninja-build
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(sdl3) >= 3.2.0
BuildRequires:  pkgconfig(libavcodec) >= 60.3
BuildRequires:  pkgconfig(libavformat) >= 60.3
BuildRequires:  pkgconfig(libavutil) >= 58.2
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libavdevice)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libdrm)

Requires:       android-tools
Requires:       hicolor-icon-theme

%description
scrcpy provides display and control of Android devices connected via
USB or over TCP/IP. It does not require any root access on the device
and works on GNU/Linux, Windows, and macOS.

%prep
%autosetup

%build
%meson -Dprebuilt_server=%{SOURCE1}
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-console.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-console.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/disconnected.png
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Oct 08 2026 boobaa <xenialv7@gmail.com> - 5.0.1-1
- Initial package for Fedora COPR
