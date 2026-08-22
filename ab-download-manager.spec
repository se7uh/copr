%global debug_package %{nil}

Name:           ab-download-manager
Version:        1.10.1
Release:        1%{?dist}
Summary:        A Download Manager that speeds up your downloads

License:        Apache-2.0
URL:            https://github.com/amir1376/ab-download-manager
Source0:        %{url}/releases/download/v%{version}/ABDownloadManager_%{version}_linux_x64.tar.gz
Source1:        https://raw.githubusercontent.com/amir1376/%{name}/v%{version}/LICENSE

BuildRequires:  desktop-file-utils

Requires:       gtk3
Requires:       hicolor-icon-theme
Recommends:     libappindicator-gtk3

%description
AB Download Manager is a desktop download manager that speeds up your
downloads. It features a clean UI, multi-threaded download acceleration,
browser integration, speed limiter, download queue management, and a CLI.

%prep
%setup -q -n ABDownloadManager
cp %{SOURCE1} LICENSE

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -a bin lib %{buildroot}%{_libdir}/%{name}/

# Executables
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/bin/ABDownloadManager %{buildroot}%{_bindir}/ab-download-manager
ln -s %{_libdir}/%{name}/bin/ABDownloadManagerCli %{buildroot}%{_bindir}/abdm

# Desktop integration
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -D -p -m 0644 lib/ABDownloadManager.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

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
%{_bindir}/abdm
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%changelog
* Sat Aug 22 2026 boobaa <xenialv7@gmail.com> - 1.10.1-1
- Initial package for Fedora COPR
