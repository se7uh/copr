%global debug_package %{nil}
%global rust_toolchain rust >= 1.95.0

Name:           zellij
Version:        0.46.0
Release:        1%{?dist}
Summary:        A terminal workspace with batteries included

License:        MIT
URL:            https://github.com/zellij-org/zellij
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconfig
BuildRequires:  cmake
BuildRequires:  protobuf-compiler
BuildRequires:  %{rust_toolchain}
BuildRequires:  cargo
BuildRequires:  rust-std-static-wasm32-wasip1
BuildRequires:  desktop-file-utils
BuildRequires:  appstream

%description
Zellij is a workspace aimed at developers, ops-oriented people and anyone who
loves the terminal. Similar programs are sometimes called "Terminal
Multiplexers".

Zellij is designed around the philosophy that one must not sacrifice simplicity
for power, taking pride in its great experience out of the box as well as the
advanced features it places at its users' fingertips.

%prep
%autosetup

%build
# Wasm plugins: clear RUSTFLAGS (Fedora's -specs flag breaks lld)
RUSTFLAGS="" cargo build --release --target wasm32-wasip1 \
  -p bars -p strider -p session-manager -p configuration \
  -p plugin-manager -p about -p share -p multiple-select \
  -p layout-manager -p prompt -p context-menu

mkdir -p zellij-utils/assets/plugins/
cp target/wasm32-wasip1/release/*.wasm zellij-utils/assets/plugins/

# Main binary (with default RPM RUSTFLAGS)
cargo build --release -p zellij

%install
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Desktop entry and AppStream metadata
install -D -p -m 0644 assets/dev.zellij.Zellij.desktop %{buildroot}%{_datadir}/applications/dev.zellij.Zellij.desktop
install -D -p -m 0644 assets/dev.zellij.Zellij.metainfo.xml %{buildroot}%{_metainfodir}/dev.zellij.Zellij.metainfo.xml

# Icons
for size in 128 256 512; do
  install -D -p -m 0644 zellij-utils/assets/icons/logo${size}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/dev.zellij.Zellij.png
done

# Completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
%{buildroot}%{_bindir}/%{name} setup --generate-completion bash \
  > %{buildroot}%{_datadir}/bash-completion/completions/%{name} 2>/dev/null || :

mkdir -p %{buildroot}%{_datadir}/zsh/site-functions/
%{buildroot}%{_bindir}/%{name} setup --generate-completion zsh \
  > %{buildroot}%{_datadir}/zsh/site-functions/_%{name} 2>/dev/null || :

mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d/
%{buildroot}%{_bindir}/%{name} setup --generate-completion fish \
  > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish 2>/dev/null || :

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/dev.zellij.Zellij.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/dev.zellij.Zellij.metainfo.xml

%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/dev.zellij.Zellij.desktop
%{_metainfodir}/dev.zellij.Zellij.metainfo.xml
%{_datadir}/icons/hicolor/*/apps/dev.zellij.Zellij.png
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%dir %{_datadir}/fish
%dir %{_datadir}/fish/vendor_completions.d
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%changelog
* Thu Nov 12 2026 boobaa <xenialv7@gmail.com> - 0.46.0-1
- Update to 0.46.0
- Package desktop entry, icons, and AppStream metadata per PACKAGING_DESKTOP.md
- Update plugin list: replace individual bars/link with bars, add prompt and context-menu

* Sat Aug 29 2026 boobaa <xenialv7@gmail.com> - 0.45.1-1
- Update to 0.45.1
- Drop disable-auto-enter-search-mode-on-scroll.patch (supported natively via scroll_mode_sync config)

* Mon Aug 24 2026 boobaa <xenialv7@gmail.com> - 0.45.0-2
- Disable entering search/scroll mode when scrolling (restore v0.44 scroll behavior)

* Fri Aug 21 2026 boobaa <xenialv7@gmail.com> - 0.45.0-1
- Update to 0.45.0
- Drop xtask manpage generation (removed upstream)
- Disable debuginfo package to optimize build and signing time

* Mon Jun 29 2026 boobaa <xenialv7@gmail.com> - 0.44.3-1
- Initial package for Fedora COPR
