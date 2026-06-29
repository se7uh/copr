%global rust_toolchain rust >= 1.93.0

Name:           ouch
Version:        0.8.0
Release:        1%{?dist}
Summary:        Painless compression and decompression in the terminal

License:        MIT
URL:            https://github.com/ouch-org/ouch
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  clang-devel
BuildRequires:  %{rust_toolchain}
BuildRequires:  cargo

%description
ouch stands for Obvious Unified Compression Helper. It is a CLI tool for
compressing and decompressing various formats including tar, zip, 7z, gz,
zstd, xz, lzma, bzip2, lz4, rar, and brotli.

%prep
%autosetup

%build
cargo build --release %{?_smp_flags}

%install
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Install shell completions
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
%{buildroot}%{_bindir}/%{name} completion bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name} 2>/dev/null || :

mkdir -p %{buildroot}%{_datadir}/zsh/site-functions/
%{buildroot}%{_bindir}/%{name} completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name} 2>/dev/null || :

mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d/
%{buildroot}%{_bindir}/%{name} completion fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish 2>/dev/null || :

%check
cargo test --release || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
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
* Sun Jun 29 2026 boobaa <xenialv7@gmail.com> - 0.8.0-1
- Initial package for Fedora COPR
