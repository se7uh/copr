Name:           lazygit
Version:        0.65.0
Release:        1%{?dist}
Summary:        Simple terminal UI for git commands

License:        MIT
URL:            https://github.com/jesseduffield/lazygit
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  golang

%description
lazygit provides a simple terminal user interface for common git operations.

%prep
%autosetup

%build
export CGO_CPPFLAGS="%{optflags}"
export CGO_CFLAGS="%{optflags}"
export CGO_CXXFLAGS="%{optflags}"
export GOFLAGS="-buildmode=pie -trimpath -modcacherw"

go build \
    -ldflags "\
      -linkmode external \
      -extldflags '%{build_ldflags}' \
      -X main.date=$(date -u +%Y-%m-%dT%H:%M:%SZ) \
      -X main.buildSource=copr \
      -X main.version=%{version} \
      -X main.commit=v%{version} \
    "

%install
install -D -p -m 0755 lazygit %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md docs
%{_bindir}/%{name}

%changelog
* Sun Sep 06 2026 boobaa <boobaa@users.noreply.github.com> - 0.65.0-1
- Update to 0.65.0
- Dim UI when inactive, allow typing to filter menus, and filter worktrees by branch
- Fix scroll into view, visual glitch when moving rebase todos, and async diff crash

* Thu Aug 13 2026 boobaa <boobaa@users.noreply.github.com> - 0.64.1-1
- Update to 0.64.1
- Fixes filtering mode transitions, stash race, PR list refresh, and other regressions

* Mon Aug 10 2026 boobaa <boobaa@users.noreply.github.com> - 0.64.0-1
- Initial package
