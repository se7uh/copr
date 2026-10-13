%global debug_package %{nil}
%global __strip /bin/true
%global __brp_strip %{nil}
%global __brp_strip_comment_note %{nil}
%global __brp_strip_static_archive %{nil}
%global __brp_python_bytecompile %{nil}
%global __brp_check_rpaths %{nil}
%undefine __brp_mangle_shebangs
%global __brp_mangle_shebangs_exclude_from ^%{_libdir}/%{name}/.*$
%global _build_id_links none
%undefine _missing_build_ids_terminate_build
%global __provides_exclude_from ^%{_libdir}/%{name}/.*$
%global __requires_exclude_from ^%{_libdir}/%{name}/.*$

Name:           anki-bin
Version:        26.09.3
Release:        1%{?dist}
Summary:        Powerful, intelligent flash cards (precompiled binary release)

License:        AGPL-3.0-or-later
URL:            https://github.com/ankitects/anki
Source0:        %{url}/releases/download/%{version}/anki-%{version}-linux-x86_64.tar.zst

ExclusiveArch:  x86_64

BuildRequires:  tar
BuildRequires:  zstd
BuildRequires:  desktop-file-utils

Requires:       fontconfig
Requires:       freetype
Requires:       glibc >= 2.35
Requires:       hicolor-icon-theme
Requires:       libGL
Requires:       libX11
Requires:       libXcomposite
Requires:       libXcursor
Requires:       libXi
Requires:       libXinerama
Requires:       libXrandr
Requires:       libXtst
Requires:       libxkbcommon
Requires:       libxkbcommon-x11
Requires:       nss
Requires:       shared-mime-info
Requires:       xcb-util-cursor
Requires:       xcb-util-image
Requires:       xcb-util-keysyms
Requires:       xcb-util-renderutil
Requires:       xcb-util-wm
Requires:       xdg-utils
Recommends:     lame
Recommends:     mpv

Provides:       anki = %{version}-%{release}
Provides:       anki-bin = %{version}-%{release}

%description
Anki is a spaced-repetition flashcard program that makes remembering things easy.
Because it's a lot more efficient than traditional study methods, you can either
greatly decrease your time spent studying, or greatly increase the amount you learn.

This package provides the official precompiled binary release from upstream,
packaged for Fedora RPM systems.

%prep
%setup -c -T
tar --zstd -xf %{SOURCE0}
mv anki-*-linux-*.tar/* .
rmdir anki-*-linux-*.tar

%build
# Precompiled binary, no compilation required

%install
export QA_RPATHS=0x0002

# Main application bundle in %{_libdir}/%{name}
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -a anki app app_packages python %{buildroot}%{_libdir}/%{name}/

# Binary symlinks in /usr/bin
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libdir}/%{name}/anki %{buildroot}%{_bindir}/anki
ln -s %{_libdir}/%{name}/anki %{buildroot}%{_bindir}/%{name}

# Desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
install -p -m 0644 anki.desktop %{buildroot}%{_datadir}/applications/anki.desktop

# Pixmaps / Icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -p -m 0644 anki.png %{buildroot}%{_datadir}/pixmaps/anki.png
install -p -m 0644 anki.xpm %{buildroot}%{_datadir}/pixmaps/anki.xpm

# MIME package
mkdir -p %{buildroot}%{_datadir}/mime/packages
install -p -m 0644 anki.xml %{buildroot}%{_datadir}/mime/packages/anki.xml

# Man page
mkdir -p %{buildroot}%{_mandir}/man1
install -p -m 0644 anki.1 %{buildroot}%{_mandir}/man1/anki.1

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/anki.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/anki
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/anki.desktop
%{_datadir}/pixmaps/anki.png
%{_datadir}/pixmaps/anki.xpm
%{_datadir}/mime/packages/anki.xml
%{_mandir}/man1/anki.1*

%changelog
* Tue Oct 13 2026 boobaa <xenialv7@gmail.com> - 26.09.3-1
- Initial package for Fedora COPR
