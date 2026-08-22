%global debug_package %{nil}
%global __strip /bin/true

Name:           ab-download-manager
Version:        1.10.1
Release:        1%{?dist}
Summary:        A Download Manager that speeds up your downloads

License:        Apache-2.0
URL:            https://github.com/amir1376/ab-download-manager
Source0:        %{url}/releases/download/v%{version}/ABDownloadManager_%{version}_linux_x64.tar.gz
Source1:        %{url}/releases/download/v%{version}/ABDownloadManager_%{version}_linux_arm64.tar.gz
Source2:        https://raw.githubusercontent.com/amir1376/%{name}/v%{version}/LICENSE

ExclusiveArch:  x86_64 aarch64

BuildRequires:  desktop-file-utils

Requires:       alsa-lib
Requires:       fontconfig
Requires:       freetype
Requires:       glibc
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libXext
Requires:       libXi
Requires:       libXrender
Requires:       libXtst
Requires:       libglvnd-glx
Requires:       zlib

Recommends:     libappindicator-gtk3

%description
AB Download Manager is a modern desktop download manager that speeds up your
downloads. It features a clean Compose Multiplatform UI, multi-threaded
download acceleration, browser integration, speed limiter, download queue
management, and a companion CLI.

%prep
%setup -q -c -T
%ifarch x86_64
tar -xzf %{SOURCE0} --strip-components=1
%endif
%ifarch aarch64
tar -xzf %{SOURCE1} --strip-components=1
%endif
cp %{SOURCE2} LICENSE

%build
# Precompiled release binaries

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -a bin lib %{buildroot}%{_libdir}/%{name}/

# Ensure executable permissions
chmod 0755 %{buildroot}%{_libdir}/%{name}/bin/*
chmod 0755 %{buildroot}%{_libdir}/%{name}/lib/libapplauncher.so

# Symlink binaries into %{_bindir}
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/bin/ABDownloadManager %{buildroot}%{_bindir}/ab-download-manager
ln -s %{_libdir}/%{name}/bin/ABDownloadManager %{buildroot}%{_bindir}/abdownloadmanager
ln -s %{_libdir}/%{name}/bin/ABDownloadManager %{buildroot}%{_bindir}/ABDownloadManager
ln -s %{_libdir}/%{name}/bin/ABDownloadManagerCli %{buildroot}%{_bindir}/ab-download-manager-cli
ln -s %{_libdir}/%{name}/bin/ABDownloadManagerCli %{buildroot}%{_bindir}/abdm
ln -s %{_libdir}/%{name}/bin/ABDownloadManagerCli %{buildroot}%{_bindir}/ABDownloadManagerCli

# Install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -D -p -m 0644 lib/ABDownloadManager.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -D -p -m 0644 lib/ABDownloadManager.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -p -m 0644 lib/ABDownloadManager.png %{buildroot}%{_datadir}/pixmaps/ABDownloadManager.png

# Install desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=AB Download Manager
Comment=Manage and organize your download files better than before
GenericName=Download Manager
Exec=ab-download-manager %U
Icon=ab-download-manager
Terminal=false
Type=Application
Categories=Network;FileTransfer;
StartupWMClass=com-abdownloadmanager-desktop-AppKt
MimeType=x-scheme-handler/abdm;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%{_bindir}/ab-download-manager
%{_bindir}/abdownloadmanager
%{_bindir}/ABDownloadManager
%{_bindir}/ab-download-manager-cli
%{_bindir}/abdm
%{_bindir}/ABDownloadManagerCli
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/ABDownloadManager.png

%changelog
* Sat Aug 22 2026 boobaa <xenialv7@gmail.com> - 1.10.1-1
- Initial package for Fedora COPR
