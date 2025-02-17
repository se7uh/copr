%global debug_package %{nil}

Name:           bustd
Version:        0.1.1
Release:        1%{?dist}
Summary:        Lightweight process killer daemon for out-of-memory scenarios

License:        MIT
URL:            https://github.com/vrmiguel/bustd
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  rust >= 1.56.0
BuildRequires:  cargo
BuildRequires:  systemd-rpm-macros

%description
bustd is a lightweight process killer daemon for out-of-memory scenarios for Linux.
It uses adaptive sleep times during memory polling and checks Pressure Stall
Information (PSI) to detect memory pressure.

%prep
%autosetup

%build
cargo build --release

%install
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Install systemd service
mkdir -p %{buildroot}%{_unitdir}
cat > %{buildroot}%{_unitdir}/%{name}.service << EOF
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
* %{_date} %{_username} <%{_useremail}> - 0.1.1-1
- Initial package for Fedora COPR 