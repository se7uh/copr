%global debug_package %{nil}
%global __strip /bin/true
%global __brp_strip %{nil}
%global __brp_strip_comment_note %{nil}
%global __brp_strip_static_archive %{nil}

Name:           devtray
Version:        2.1.3
Release:        2%{?dist}
Summary:        A lightweight system tray application to manage background development services

License:        MIT
URL:            https://github.com/wdsfgd/devtray
Source0:        %{url}/releases/download/v%{version}/%{name}-v%{version}-linux-x86_64.tar.gz
Source1:        https://raw.githubusercontent.com/wdsfgd/%{name}/v%{version}/assets/icon.svg

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils

Requires:       fontconfig
Requires:       freetype
Requires:       hicolor-icon-theme

%description
DevTray is a lightweight, ultra-low memory Linux system tray application for
developers to manage background development services (e.g., Node dev servers,
Docker containers, database instances).

Run long-running background tasks without keeping terminal windows open. Group
tasks by project, reorder them with intuitive move controls, view live streaming
logs, and start/stop services instantly from the system tray.

%prep
%setup -q -n %{name}-v%{version}

%build
# Precompiled binary, no compilation required

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=DevTray
GenericName=Development Service Manager
Comment=A lightweight system tray application to manage background development services
Exec=devtray
Icon=devtray
Terminal=false
Categories=Development;
Keywords=tray;service;task;process;dev;
StartupNotify=false
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -p -m 0644 assets/icon.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -p -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Sat Oct 10 2026 boobaa <xenialv7@gmail.com> - 2.1.3-2
- Provide explicit desktop entry with GenericName and Keywords

* Sat Oct 10 2026 boobaa <xenialv7@gmail.com> - 2.1.3-1
- Initial package for Fedora COPR
