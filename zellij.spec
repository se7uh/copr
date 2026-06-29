%global rust_toolchain rust >= 1.92.0

Name:           zellij
Version:        0.44.3
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
  -p compact-bar -p status-bar -p strider -p tab-bar \
  -p fixture-plugin-for-tests -p session-manager -p configuration \
  -p plugin-manager -p about -p multiple-select -p share \
  -p layout-manager -p link

mkdir -p zellij-utils/assets/plugins/
cp target/wasm32-wasip1/release/*.wasm zellij-utils/assets/plugins/

# Main binary (with default RPM RUSTFLAGS)
cargo build --release -p zellij

# Man page
cargo install mandown --locked
export PATH="$HOME/.cargo/bin${PATH:+:${PATH}}"
cargo xtask manpage

%install
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -D -m 0644 assets/man/zellij.1 %{buildroot}%{_mandir}/man1/%{name}.1

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

%files
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
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
* Mon Jun 29 2026 boobaa <xenialv7@gmail.com> - 0.44.3-1
- Initial package for Fedora COPR
