%global debug_package %{nil}

Name:           floorp
Version:        12.21.1
Release:        1%{?dist}
Summary:        Floorp Web Browser

License:        MPL-2.0
URL:            https://github.com/Floorp-Projects/Floorp
Source0:        %{url}/releases/download/v%{version}/floorp-linux-x86_64.tar.xz
Source1:        %{url}/releases/download/v%{version}/floorp-linux-aarch64.tar.xz
Source2:        https://raw.githubusercontent.com/Floorp-Projects/Floorp/v%{version}/LICENSE

ExclusiveArch:  x86_64 aarch64

BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  desktop-file-utils
%ifarch x86_64
BuildRequires:  patchelf
%endif

Requires:       gtk3
Requires:       hicolor-icon-theme

%description
Floorp is a customizable and privacy-focused web browser based on Firefox.
It is developed by the Floorp Projects community, offering enhanced
customization, vertical tabs, workspaces, and robust privacy features.

This package provides the official precompiled binary release from upstream.

%prep
%ifarch x86_64
%setup -q -T -b 0 -n floorp
%endif
%ifarch aarch64
%setup -q -T -b 1 -n floorp
%endif
cp %{SOURCE2} LICENSE

%build
# Precompiled binary release, no compilation required

%install
mkdir -p %{buildroot}/opt/%{name}
cp -a * %{buildroot}/opt/%{name}/
rm -f %{buildroot}/opt/%{name}/LICENSE

# Executable symlink
mkdir -p %{buildroot}%{_bindir}
ln -s /opt/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# Disable internal updater via distribution policy
mkdir -p %{buildroot}/opt/%{name}/distribution
cat > %{buildroot}/opt/%{name}/distribution/policies.json << 'EOF'
{
  "policies": {
    "DisableAppUpdate": true
  }
}
EOF

# Fix RPATH for ONNX runtime library on x86_64
%ifarch x86_64
if [ -f %{buildroot}/opt/%{name}/libonnxruntime.so ]; then
    patchelf --set-rpath '$ORIGIN' %{buildroot}/opt/%{name}/libonnxruntime.so
fi
%endif

# Desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Name=Floorp
GenericName=Web Browser
Comment=Browse the Web
Exec=floorp %u
Icon=floorp
Terminal=false
Type=Application
MimeType=text/html;text/xml;application/xhtml+xml;application/vnd.mozilla.xul+xml;text/mml;x-scheme-handler/http;x-scheme-handler/https;
Categories=Network;WebBrowser;
StartupNotify=true
StartupWMClass=floorp-default
Actions=new-window;new-private-window;

[Desktop Action new-window]
Name=Open a New Window
Exec=floorp --new-window %u

[Desktop Action new-private-window]
Name=Open a New Private Window
Exec=floorp --private-window %u
EOF

# Icons
for size in 16 32 48 64 128; do
    if [ -f "browser/chrome/icons/default/default${size}.png" ]; then
        install -D -p -m 0644 "browser/chrome/icons/default/default${size}.png" \
            "%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png"
    fi
done
install -D -p -m 0644 browser/chrome/icons/default/default128.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE
%{_bindir}/%{name}
/opt/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Thu Nov 05 2026 boobaa <xenialv7@gmail.com> - 12.21.1-1
- Update to 12.21.1
- Includes Firefox 159.0.1 security fixes
- Disable Mozilla-sponsored shortcuts and tile delivery by default

* Mon Nov 02 2026 boobaa <xenialv7@gmail.com> - 12.21.0-5
- Ponytail cleanup: drop wrapper script, use direct symlink to fix double-launch bug
- Remove redundant legacy ~/.floorp migration and manual XDG injection
- Keep self-contained icons from tarball with pixmaps fallback
