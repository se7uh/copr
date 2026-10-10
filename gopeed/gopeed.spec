%global debug_package %{nil}
%global __requires_exclude ^(lib.*_plugin|libflutter_linux_gtk|libgopeed|libapp)\\.so

Name:           gopeed
Version:        1.9.3
Release:        2%{?dist}
Summary:        A fast, modern download manager for HTTP, BitTorrent, Magnet, and ed2k

License:        GPL-3.0
URL:            https://github.com/GopeedLab/gopeed
Source0:        %{url}/releases/download/v%{version}/Gopeed-v%{version}-linux-amd64.rpm
Source1:        https://raw.githubusercontent.com/GopeedLab/%{name}/v%{version}/LICENSE

ExclusiveArch:  x86_64

BuildRequires:  cpio
BuildRequires:  desktop-file-utils
BuildRequires:  rpm

Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       keybinder3
Recommends:     libayatana-appindicator-gtk3

%description
Gopeed (Go Speed) is a high-speed, modern download manager that supports HTTP,
BitTorrent, Magnet links, and ed2k protocols. It features a clean Flutter GUI,
extension ecosystem, customizable connection settings, and system tray integration.

%prep
%setup -c -T
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} LICENSE

%build
# Precompiled Flutter application, no build step required

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -a opt/gopeed/* %{buildroot}%{_libdir}/%{name}/

# Fix permissions
chmod 0755 %{buildroot}%{_libdir}/%{name}/%{name}
chmod 0755 %{buildroot}%{_libdir}/%{name}/lib/*.so
chmod 0755 %{buildroot}%{_libdir}/%{name}/data/flutter_assets/assets/exec/* 2>/dev/null || :

# Executable symlink
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# Desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Gopeed
GenericName=Download Manager
Comment=A fast, modern download manager for HTTP, BitTorrent, Magnet, and ed2k
Exec=gopeed %U
Icon=gopeed
Terminal=false
Categories=Network;FileTransfer;
MimeType=x-scheme-handler/gopeed;x-scheme-handler/magnet;application/x-bittorrent;
StartupWMClass=gopeed
EOF

# Icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -D -p -m 0644 usr/share/icons/hicolor/scalable/apps/%{name}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -D -p -m 0644 opt/gopeed/data/flutter_assets/assets/icon/icon_512.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%changelog
* Sat Oct 10 2026 boobaa <xenialv7@gmail.com> - 1.9.3-2
- Fix missing provides for internal Flutter and plugin shared libraries

* Sat Oct 10 2026 boobaa <xenialv7@gmail.com> - 1.9.3-1
- Initial package for Fedora COPR (x86_64)
