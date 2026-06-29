%global rust_toolchain rust >= 1.56.0

Name:           bustd
Version:        0.1.1
Release:        2%{?dist}
Summary:        Lightweight process killer daemon for out-of-memory scenarios

License:        MIT
URL:            https://github.com/vrmiguel/bustd
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  %{rust_toolchain}
BuildRequires:  cargo
BuildRequires:  systemd-rpm-macros

%description
bustd is a lightweight process killer daemon for out-of-memory scenarios
for Linux. It uses adaptive sleep times during memory polling and checks
Pressure Stall Information (PSI) to detect memory pressure.

%prep
%autosetup

%build
cargo build --release %{?_smp_flags}

%install
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Install systemd service
mkdir -p %{buildroot}%{_unitdir}
cat > %{buildroot}%{_unitdir}/%{name}.service << 'EOF'
[Unit]
Description=Lightweight process killer daemon for OOM scenarios
Documentation=https://github.com/vrmiguel/bustd

[Service]
ExecStart=%{_bindir}/%{name} --no-daemon
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

%check
cargo test --release || :

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Sun Jun 29 2026 boobaa <xenialv7@gmail.com> - 0.1.1-2
- Initial package for Fedora COPR
- Fix Source0 URL format and changelog macros