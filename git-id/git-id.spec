%global rust_toolchain rust >= 1.85

Name:           git-id
Version:        1.1.2
Release:        1%{?dist}
Summary:        Git Account Switcher - manage multiple Git accounts on one machine

License:        MIT
URL:            https://github.com/se7uh/git-id
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  %{rust_toolchain}
BuildRequires:  cargo

%description
A command-line tool to manage any number of Git accounts on one
machine. Store account details (username, email, SSH keys) in a TOML config
file and switch between them with a single command. Supports any git host,
rewrites origin remote URLs, and manages SSH keys and config stanzas.

%prep
%autosetup

%build
cargo build --release %{?_smp_flags}

%install
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

# Generate shell completions (git-id completions <shell> is a real runtime subcommand)
# The CLI writes to user home dirs, so we use a temporary HOME with stub rc files
export HOME=%{buildroot}/tmp-home
mkdir -p "$HOME"/.local/share/bash-completion/completions
mkdir -p "$HOME"/.zfunc
mkdir -p "$HOME"/.config/fish/completions
touch "$HOME"/.zshrc "$HOME"/.bashrc

%{buildroot}%{_bindir}/%{name} completions bash || :
%{buildroot}%{_bindir}/%{name} completions zsh || :
%{buildroot}%{_bindir}/%{name} completions fish || :

# Bash
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
cp "$HOME"/.local/share/bash-completion/completions/%{name} \
  %{buildroot}%{_datadir}/bash-completion/completions/%{name}

# Zsh (uses write_completion_zsh with custom _git_id_accounts helper)
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions/
cp "$HOME"/.zfunc/_%{name} \
  %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

# Fish
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d/
cp "$HOME"/.config/fish/completions/%{name}.fish \
  %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

rm -rf "$HOME"

%files
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
* Tue Jun 30 2026 boobaa <xenialv7@gmail.com> - 1.1.2-1
- Initial package for Fedora COPR
