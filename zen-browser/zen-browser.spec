%global             full_name zen-browser
%global             application_name zen
# Pre-built binary — no compilation, so no debuginfo to generate
%global             debug_package %{nil}

Name:               zen-browser
Version:            1.21.9b
Release:            1%{?dist}
Summary:            Zen Browser — a calm, Firefox-based web browser

License:            MPL-2.0
URL:                https://github.com/zen-browser/desktop

Source0:            https://github.com/zen-browser/desktop/releases/download/%{version}/zen.linux-x86_64.tar.xz
Source1:            https://github.com/zen-browser/desktop/releases/download/%{version}/zen.linux-aarch64.tar.xz
Source2:            %{full_name}.desktop
Source3:            policies.json
Source4:            %{full_name}

ExclusiveArch:      x86_64 aarch64

%ifarch x86_64
BuildRequires:      patchelf
%endif

Recommends:         (plasma-browser-integration if plasma-workspace)
Recommends:         (gnome-browser-connector if gnome-shell)

Requires(post):     gtk-update-icon-cache
Conflicts:          zen-browser-avx2, zen-browser-aarch64

Provides:           zen-browser-aarch64 = %{version}-%{release}
Obsoletes:          zen-browser-aarch64 < 1.21.4b

Provides:           zen-browser-avx2 = %{version}-%{release}
Obsoletes:          zen-browser-avx2 < 1.0.2.b.3-3

%description
Zen Browser is a fork of Firefox that aims to improve the browsing
experience by focusing on a simple, performant, private and beautifully
designed browser. It includes features like workspaces, vertical tabs,
and split view — giving you a calmer, more organised web experience.

This package downloads the official upstream pre-built binary and
bundles it for Fedora/RHEL. No code modifications are made; the binary
is used as-is from the upstream release.

Bugs related to Zen should be reported upstream at:
  https://github.com/zen-browser/desktop/issues

%prep
%ifarch x86_64
%setup -q -T -b 0 -n %{application_name}
%endif
%ifarch aarch64
%setup -q -T -b 1 -n %{application_name}
%endif

%install
%__rm -rf %{buildroot}

%__install -d %{buildroot}{/opt/%{application_name},%{_bindir},%{_datadir}/applications,%{_datadir}/icons/hicolor/128x128/apps,%{_datadir}/icons/hicolor/64x64/apps,%{_datadir}/icons/hicolor/48x48/apps,%{_datadir}/icons/hicolor/32x32/apps,%{_datadir}/icons/hicolor/16x16/apps}

%__cp -r * %{buildroot}/opt/%{application_name}
%__install -D -m 0644 %{SOURCE2} -t %{buildroot}%{_datadir}/applications
%__install -D -m 0444 %{SOURCE3} -t %{buildroot}/opt/%{application_name}/distribution
%__install -D -m 0755 %{SOURCE4} -t %{buildroot}%{_bindir}

%ifarch x86_64
patchelf --set-rpath '$ORIGIN' %{buildroot}/opt/%{application_name}/libonnxruntime.so
%endif

%__ln_s ../../../../../../opt/%{application_name}/browser/chrome/icons/default/default128.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/browser/chrome/icons/default/default64.png \
    %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/browser/chrome/icons/default/default48.png \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/browser/chrome/icons/default/default32.png \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%__ln_s ../../../../../../opt/%{application_name}/browser/chrome/icons/default/default16.png \
    %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png

%post
gtk-update-icon-cache -f -t %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_datadir}/applications/%{full_name}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{full_name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{full_name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{full_name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{full_name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{full_name}.png
%{_bindir}/%{full_name}
/opt/%{application_name}

%changelog
* Mon Jul 27 2026 boobaa <xenialv7@gmail.com> - 1.21.9b-1
- Initial package based on SnenxyTengoku's spec work.
