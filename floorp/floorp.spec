%global debug_package %{nil}

Name:           floorp
Version:        12.21.0
Release:        3%{?dist}
Summary:        Floorp Web Browser (precompiled binary release)

License:        MPL-2.0
URL:            https://github.com/Floorp-Projects/Floorp
Source0:        %{url}/releases/download/v%{version}/floorp-linux-x86_64.tar.xz
Source1:        %{url}/releases/download/v%{version}/floorp-linux-aarch64.tar.xz
Source2:        https://raw.githubusercontent.com/Floorp-Projects/Floorp/v%{version}/LICENSE
Source3:        https://raw.githubusercontent.com/Floorp-Projects/Floorp/v%{version}/static/installers/stub-win64-installer/src-tauri/icons/icon.png
Source4:        https://raw.githubusercontent.com/Floorp-Projects/Floorp/v%{version}/static/installers/stub-win64-installer/src-tauri/icons/128x128@2x.png

ExclusiveArch:  x86_64 aarch64

BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  desktop-file-utils
%ifarch x86_64
BuildRequires:  patchelf
%endif

Requires:       gtk3
Requires:       hicolor-icon-theme

Recommends:     (plasma-browser-integration if plasma-workspace)
Recommends:     (gnome-browser-connector if gnome-shell)

Provides:       floorp = %{version}-%{release}
Provides:       floorp-bin = %{version}-%{release}

%description
Floorp is a customizable and privacy-focused web browser based on Firefox.
It is developed by the Floorp Projects community, offering enhanced
customization, vertical tabs, workspaces, and robust privacy features.

This package provides the official precompiled binary release from upstream,
packaged for Fedora RPM systems.

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

# Launcher wrapper script
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/usr/bin/bash

# Enable Wayland by default if running in a Wayland session
if [ -z "$MOZ_DISABLE_WAYLAND" ]; then
    if [ "$XDG_SESSION_TYPE" = "wayland" ] || { [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] && [ -n "$WAYLAND_DISPLAY" ]; }; then
        export MOZ_ENABLE_WAYLAND=1
        export MOZ_DBUS_REMOTE=1
    fi
fi

# KDE Plasma browser integration symlink
if [ "$XDG_CURRENT_DESKTOP" = "KDE" ] && [ ! -e "${HOME}/.floorp/native-messaging-hosts/org.kde.plasma.browser_integration.json" ]; then
    mkdir -p "${HOME}/.floorp/native-messaging-hosts"
    for host_dir in /usr/lib64/mozilla/native-messaging-hosts /usr/lib/mozilla/native-messaging-hosts; do
        if [ -r "${host_dir}/org.kde.plasma.browser_integration.json" ]; then
            ln -sf "${host_dir}/org.kde.plasma.browser_integration.json" "${HOME}/.floorp/native-messaging-hosts/org.kde.plasma.browser_integration.json"
            break
        fi
    done
fi

# GNOME Shell browser connector symlinks
if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
    mkdir -p "${HOME}/.floorp/native-messaging-hosts"
    for host_dir in /usr/lib64/mozilla/native-messaging-hosts /usr/lib/mozilla/native-messaging-hosts; do
        for json in org.gnome.browser_connector.json org.gnome.chrome_gnome_shell.json; do
            if [ -r "${host_dir}/${json}" ] && [ ! -e "${HOME}/.floorp/native-messaging-hosts/${json}" ]; then
                ln -sf "${host_dir}/${json}" "${HOME}/.floorp/native-messaging-hosts/${json}"
            fi
        done
    done
fi

export MOZ_APP_LAUNCHER="$0"

exec /opt/floorp/floorp "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

# Distribution policy: disable internal auto-updater
mkdir -p %{buildroot}/opt/%{name}/distribution
cat > %{buildroot}/opt/%{name}/distribution/policies.json << 'EOF'
{
  "policies": {
    "DisableAppUpdate": true
  }
}
EOF
chmod 0644 %{buildroot}/opt/%{name}/distribution/policies.json

# Fix RPATH on x86_64 for ONNX runtime library if present
%ifarch x86_64
if [ -f %{buildroot}/opt/%{name}/libonnxruntime.so ]; then
    patchelf --set-rpath '$ORIGIN' %{buildroot}/opt/%{name}/libonnxruntime.so
fi
%endif

# Desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << 'EOF'
[Desktop Entry]
Actions=new-window;new-private-window;profile-manager-window;
Type=Application
Name=Floorp
GenericName=Web Browser
Comment=Browse the Web
Exec=floorp --class="floorp" %u
Icon=floorp
StartupNotify=true
StartupWMClass=floorp-default
Terminal=false
MimeType=text/html;text/xml;application/xhtml+xml;application/vnd.mozilla.xul+xml;text/mml;x-scheme-handler/http;x-scheme-handler/https;
Categories=Network;WebBrowser;
Keywords=web;browser;internet;

[Desktop Action new-window]
Name=Open a New Window
Exec=floorp --class="floorp" --new-window %u

[Desktop Action new-private-window]
Name=Open a New Private Window
Exec=floorp --class="floorp" --private-window %u

[Desktop Action profile-manager-window]
Name=Open the Profile Manager
Exec=floorp --class="floorp" --ProfileManager %u
EOF

# Icons
for size in 16 32 48 64 128; do
    if [ -f "%{buildroot}/opt/%{name}/browser/chrome/icons/default/default${size}.png" ]; then
        mkdir -p "%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
        install -D -p -m 0644 "%{buildroot}/opt/%{name}/browser/chrome/icons/default/default${size}.png" \
            "%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png"
    fi
done

# High-resolution icons & pixmaps fallback
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/kbuildsycoca6 &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/kbuildsycoca6 &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/kbuildsycoca6 &>/dev/null || :

%files
%license LICENSE
%{_bindir}/%{name}
/opt/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png

%changelog
* Mon Nov 02 2026 boobaa <xenialv7@gmail.com> - 12.21.0-3
- Add 256x256, 512x512, and pixmaps fallback icons
- Add post/postun/posttrans scriptlets for gtk-update-icon-cache and kbuildsycoca6

* Mon Nov 02 2026 boobaa <xenialv7@gmail.com> - 12.21.0-2
- Remove __provides_exclude_from so bundled Mozilla libraries satisfy internal dependencies

* Mon Nov 02 2026 boobaa <xenialv7@gmail.com> - 12.21.0-1
- Initial package for Floorp (precompiled binary release)
